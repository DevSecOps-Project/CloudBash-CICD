import sys

import utils.constants
import utils.executor


def apply_deployment(k8s_path):
    try:
        file_path = ''.join([k8s_path, utils.constants.K8S.DEPLOYMENT_FILE])
        cmd = [
            'kubectl',
            'apply -f', 
            file_path
        ]
        utils.executor.execute_command(cmd)
        print('Deployment file applied')
    except Exception as e:
        print(f'Error occurred while applying the deployment file: {e}')
        sys.exit(1)

def apply_service(k8s_path):
    try:
        file_path = ''.join([k8s_path, utils.constants.K8S.SERVICE_FILE])
        cmd = [
            'kubectl',
            'apply -f', 
            file_path
        ]
        utils.executor.execute_command(cmd)
        print('Service file applied')
    except Exception as e:
        print(f'Error occurred while applying the service file: {e}')
        sys.exit(1)
