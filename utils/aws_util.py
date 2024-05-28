import sys
import utils.exe_util


def get_latest_image_version(repository_name, aws_region):
    try:
        result = utils.exe_util.execute_command([
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
