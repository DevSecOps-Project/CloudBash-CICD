import sys

import utils.aws_util
import utils.docker_util
import utils.executor


if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            print('Usage: python build_image.py <Dockerfile path>')
            sys.exit(1)
        dockerfile_path = sys.argv[1]
        latest_ver = utils.aws_util.get_latest_image_version()
        print(f'Latest image version: v{latest_ver}')
        new_docker_tag = utils.docker_util.increment_tag(latest_ver)
        utils.docker_util.build_docker_image(dockerfile_path, new_docker_tag)
        tagged_image = utils.docker_util.tag_docker_image(new_docker_tag)
        print(f'NEW_DOCKER_TAG={new_docker_tag}')
        print(f'TAGGED_IMAGE={tagged_image}')
    except Exception as e:
        print(f"Error occurred while building the image: {e}")
        sys.exit(1)
