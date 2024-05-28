import sys

import utils.aws_util
import utils.docker_util
import utils.executor


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('Usage: python build_docker_image.py <Dockerfile path> <repository name> <image name> <aws region>')
        sys.exit(1)
    dockerfile_path = sys.argv[1]
    latest_ver = utils.aws_util.get_latest_image_version()
    print(f'Latest image version: v{latest_ver}')
    new_tag = utils.docker_util.increment_tag(latest_ver)
    utils.docker_util.build_docker_image(dockerfile_path, new_tag)
