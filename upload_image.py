import sys

import utils.aws_util
import utils.constants
import utils.docker_util


if __name__ == "__main__":
    try:
        docker_tag = utils.aws_util.get_latest_image_version()
        new_docker_tag = utils.docker_util.increment_tag(docker_tag)
        tagged_image = utils.docker_util.tag_docker_image(new_docker_tag)
        utils.aws_util.ecr_authenticate()
        utils.docker_util.push_docker_image_to_ecr(tagged_image)
        print("Docker image uploaded successfully to ECR.")
    except Exception as e:
        print(f"Error occurred while uploading Docker image to ECR: {e}")
        sys.exit(1)
