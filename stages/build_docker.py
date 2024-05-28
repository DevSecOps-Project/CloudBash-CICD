import os
import subprocess
import sys

def get_latest_image_version(repository_name, aws_region):
    try:
        command = [
            'aws', 'ecr', 'describe-images',
            '--repository-name', repository_name,
            '--region', aws_region,
            '--output', 'text',
            '--query', '"sort_by(imageDetails,&imagePushedAt)[-1].imageTags[0]"'
        ]
        cmd = ' '.join(command)
        result = os.popen(cmd).read()
        striped_tag = result.strip(" v'\n'")
        latest_tag = float(striped_tag)
        print(f'Latest image version: {latest_tag}')
        return latest_tag
    except subprocess.CalledProcessError as e:
        print(f'Error occurred while retrieving latest image tag from ECR: {e.stderr}', file=sys.stderr)
        sys.exit(1)

def increment_tag(ver):
    new_ver = (ver * 10 + 1) / 10
    new_tag = 'v' + str(new_ver)
    return new_tag

def build_docker_image(dockerfile_path, image_name, new_tag):
    try:
        # docker build --tag <image-name> <location>
        command = [
            'docker', 'build',
            '--tag', f'{image_name}:{new_tag}',
            dockerfile_path,
        ]
        print(f'Running command: {" ".join(command)}')
        cmd = ' '.join(command)
        os.popen(cmd).read()
        print('Docker image built successfully.')
    except subprocess.CalledProcessError as e:
        print(f'Error occurred while building Docker image: {e.stderr}', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('Usage: python build_docker_image.py <Dockerfile path> <repository name> <image name> <aws region>')
        sys.exit(1)
    dockerfile_path = sys.argv[1]
    repository_name = sys.argv[2]
    image_name = sys.argv[3]
    aws_region = sys.argv[4]
    latest_ver = get_latest_image_version(repository_name, aws_region)
    new_tag = increment_tag(latest_ver)
    build_docker_image(dockerfile_path, image_name, new_tag)
