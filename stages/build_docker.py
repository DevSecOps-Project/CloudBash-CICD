import os
import subprocess
import sys
import re
import json

def get_latest_image_tag(repository_name, aws_region):
    try:
        command = [
            '/usr/local/aws', 'ecr', 'describe-images',
            '--repository-name', repository_name,
            '--region', aws_region,
            '--output', 'text',
            '--query', '"sort_by(imageDetails,&imagePushedAt)[-1].imageTags[0]"'
        ]
        cmd = ' '.join(command)
        result = os.system(cmd)
        latest_tag = json.loads(result.stdout.strip().strip('"'))
        print(f'Latest image tag: {latest_tag}')
        return latest_tag
    except subprocess.CalledProcessError as e:
        print(f'Error occurred while retrieving latest image tag from ECR: {e.stderr}', file=sys.stderr)
        sys.exit(1)

def increment_tag(tag):
    match = re.match(r"(\d+)$", tag)
    if match:
        new_tag = str(int(tag) + 1)
    else:
        raise ValueError(f"Invalid tag format: {tag}")
    return new_tag

def build_docker_image(dockerfile_path, image_name, new_tag):
    try:
        command = [
            'docker', 'build',
            '-t', f'{image_name}:{new_tag}',
            '-f', dockerfile_path,
            '.'
        ]
        print(f'Running command: {" ".join(command)}')
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout)
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
    latest_tag = get_latest_image_tag(repository_name, aws_region)
    new_tag = increment_tag(latest_tag)
    build_docker_image(dockerfile_path, image_name, new_tag)
