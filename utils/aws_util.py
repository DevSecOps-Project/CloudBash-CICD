import sys

import utils.constants
import utils.executor


def get_latest_image_version():
    try:
        repository_name = utils.constants.AWS.ECR_REPO
        aws_region = utils.constants.AWS.AWS_REGION
        result = utils.executor.execute_command([
            '/opt/homebrew/bin/aws', 'ecr', 'describe-images',
            '--repository-name', repository_name,
            '--region', aws_region,
            '--output', 'text',
            '--query', '"sort_by(imageDetails,&imagePushedAt)[-1].imageTags[0]"'
        ])
        striped_tag = result.strip(" v'\n'")
        if striped_tag == '':
            raise ValueError(f"failed to get the latest image version")
        latest_tag = float(striped_tag)
        return latest_tag
    except Exception as e:
        print(f'Error occurred while retrieving latest image tag from ECR: {e}')
        sys.exit(1)

def ecr_authenticate():
    try:
        aws_account_id = utils.constants.AWS.AWS_ACCOUNT_ID
        aws_region = utils.constants.AWS.AWS_REGION
        pass_stdin = f"{aws_account_id}.dkr.ecr.{aws_region}.amazonaws.com"
        utils.executor.execute_command([
            "aws", "ecr",
            "get-login-password",
            "--region", aws_region,
            "|", "docker", "login",
            "--username", "AWS",
            "--password-stdin", pass_stdin
        ])
    except Exception as e:
        print(f'Error occurred while authenticating ECR: {e}')
        sys.exit(1)
