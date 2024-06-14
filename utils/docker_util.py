import sys

import utils.constants
import utils.executor


def build_docker_image(dockerfile_path, new_tag):
    try:
        image_name = utils.constants.DOCKER.LOCAL_IMAGE_NAME
        utils.executor.execute_command([
            '/usr/local/bin/docker', 'build',
            '--tag', f'{image_name}:{new_tag}',
            dockerfile_path
        ])
    except Exception as e:
        print(f'Error occurred while building Docker image: {e}')
        sys.exit(1)

def increment_tag(docker_tag):
    new_ver = (docker_tag * 10 + 1) / 10
    new_tag = 'v' + str(new_ver)
    return new_tag

def tag_docker_image(docker_tag):
    try:
        aws_account_id = utils.constants.AWS.AWS_ACCOUNT_ID
        aws_region = utils.constants.AWS.AWS_REGION
        repository_name = utils.constants.AWS.ECR_REPO
        image_name = utils.constants.DOCKER.LOCAL_IMAGE_NAME
        ecr_uri = f"{aws_account_id}.dkr.ecr.{aws_region}.amazonaws.com/{repository_name}"
        tagged_image = f"{ecr_uri}:{docker_tag}"
        print(tagged_image)
        utils.executor.execute_command([
                "docker",
                "tag",
                f"{image_name}:{docker_tag}",
                tagged_image
        ])
        print("hello")
        return tagged_image
    except Exception as e:
        print(f'Error occurred while tagging Docker image: {e}')
        sys.exit(1)

def push_docker_image_to_ecr(tagged_image):
    try:
        utils.executor.execute_command(["docker", "push", tagged_image])
    except Exception as e:
        print(f'Error occurred while pushing Docker image to ECR: {e}')
        sys.exit(1)
