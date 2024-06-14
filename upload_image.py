import os
import sys
import time

import utils.aws_util
import utils.constants
import utils.docker_util


if __name__ == "__main__":
    try:
        tagged_image = os.getenv('TAGGED_IMAGE')
        new_docker_tag = os.getenv('NEW_DOCKER_TAG')
        if not tagged_image or not new_docker_tag:
            raise ValueError('TAGGED_IMAGE or NEW_DOCKER_TAG environment variables not set')
        utils.aws_util.ecr_authenticate()
        utils.docker_util.push_docker_image_to_ecr(tagged_image)
        new_tag = utils.aws_util.strip_version_val(new_docker_tag)
        time.sleep(10)
        if utils.aws_util.is_last_version(new_tag):
            print("Docker image uploaded successfully to ECR")
        else:
            print("Docker image upload to ECR failed")
            raise ValueError(f'image {new_docker_tag} was not found on aws')
    except Exception as e:
        print(f"Error occurred while uploading Docker image to ECR: {e}")
        sys.exit(1)
