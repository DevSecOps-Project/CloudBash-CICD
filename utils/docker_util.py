import sys

import utils.exe_util


def build_docker_image(dockerfile_path, image_name, new_tag):
    try:
        result = utils.exe_util.execute_command([
            '/usr/local/bin/docker', 'build',
            '--tag', f'{image_name}:{new_tag}',
            dockerfile_path
        ])
    except Exception as e:
        print(f'Error occurred while building Docker image: {e}')
        sys.exit(1)
