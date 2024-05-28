import sys

import utils.aws_util
import utils.docker_util
import utils.executor


def increment_tag(ver):
    new_ver = (ver * 10 + 1) / 10
    new_tag = 'v' + str(new_ver)
    return new_tag

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('Usage: python build_docker_image.py <Dockerfile path> <repository name> <image name> <aws region>')
        sys.exit(1)
    dockerfile_path = sys.argv[1]
    repository_name = sys.argv[2]
    image_name = sys.argv[3]
    aws_region = sys.argv[4]
    latest_ver = utils.aws_util.get_latest_image_version(repository_name, aws_region)
    print(f'Latest image version: v{latest_ver}')
    new_tag = increment_tag(latest_ver)
    utils.docker_util.build_docker_image(dockerfile_path, image_name, new_tag)
