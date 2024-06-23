import re
import sys

import utils.constants
import utils.executor


def k8s_apply(k8s_path, file):
    try:
        file_path = ''.join([k8s_path, file])
        cmd = [
            './kubectl',
            'apply -f',
            file_path
        ]
        output = utils.executor.execute_command(cmd)
        if ('created' in output
            or 'updated' in output
            or 'unchanged' in output):
            print(f'k8s file {file} applied')
        else:
            raise Exception
    except Exception as e:
        print(f'Error occurred while applying the k8s file: {file}, {e}')
        sys.exit(1)

def age_to_seconds(age_str):
    age_seconds = 0
    time_units = {
        's': 1,
        'm': 60,
        'h': 3600,
        'd': 86400,
        'w': 604800
    }
    pattern = re.compile(r'(\d+)([smhdw])')
    for amount, unit in pattern.findall(age_str):
        age_seconds += int(amount) * time_units[unit]
    return age_seconds

def valid_creds_secret(secret):
    try:
        cmd = ['./kubectl', 'get', 'secret', '--all-namespaces']
        output = utils.executor.execute_command(cmd)
        pattern = re.compile(r'default\s+creds-secret\s+\S+\s+\d+\s+(\S+)')
        match = pattern.search(output)
        age = match.group(1)
        if secret in output:
            one_day_seconds = 86400
            age_in_seconds = age_to_seconds(age)
            if age_in_seconds > one_day_seconds:
                print(f"Age of creds-secret ({age}) is higher than 1 day")
            else:
                print(f"Age of creds-secret ({age}) is less than 1 day")
                return True
        return False
    except Exception as e:
        print(f'Error occurred while geting secrets: {e}')
        sys.exit(1)

def setup_creds_secret():
    try:
        creds_secret = 'creds-secret'
        if valid_creds_secret(creds_secret):
            print('creds_secret exist and is valid')
            return
        cmd = ['./kubectl', 'delete', 'secret', creds_secret]
        utils.executor.execute_command(cmd)
        aws_account_id = utils.constants.AWS.AWS_ACCOUNT_ID
        aws_region = utils.constants.AWS.AWS_REGION
        pass_stdin = f"{aws_account_id}.dkr.ecr.{aws_region}.amazonaws.com"
        cmd = [
            './kubectl',
            'create secret', 'docker-registry',
            creds_secret, f'--docker-server={pass_stdin}',
            '--docker-username=AWS',
            '--docker-password=$(/opt/homebrew/bin/aws ecr get-login-password)'
        ]
        utils.executor.execute_command(cmd)
        if valid_creds_secret(creds_secret):
            print('creds_secret created successfully')
            return
        raise Exception
    except Exception as e:
        print(f'Error occurred while setting up creds secret: {e}')
        sys.exit(1)
