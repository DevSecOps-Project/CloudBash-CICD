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
            print('k8s file applied')
        else:
            raise Exception
    except Exception as e:
        print(f'Error occurred while applying the k8s file: {k8s_path}, {e}')
        sys.exit(1)

def creds_secret_exist(secret):
    try:
        cmd = ['./kubectl', 'get', 'secret', '--all-namespaces']
        # cmd = ['kubectl', 'get', 'secret', '--all-namespaces']
        output = utils.executor.execute_command(cmd)
        # re.search('default       creds-secret             kubernetes.io/dockerconfigjson   1      2d7h')
        if secret in output:
            return True
        return False
    except Exception as e:
        print(f'Error occurred while geting secrets: {e}')
        sys.exit(1)

def creds_secret_uptodate(creds_secret):
    return False

def setup_creds_secret():
    try:
        creds_secret = 'creds-secret'
        if creds_secret_exist(creds_secret):
            if creds_secret_uptodate(creds_secret):
                print('creds_secret exist')
                return
        cmd = ['./kubectl', 'delete', creds_secret]
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
        if creds_secret_exist(creds_secret):
            print('creds_secret created successfully')
            return
        raise Exception
    except Exception as e:
        print(f'Error occurred while setting up creds secret: {e}')
        sys.exit(1)
