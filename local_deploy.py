import os
import sys

import utils.aws_util
import utils.constants
import utils.docker_util
import utils.executor
import utils.k8s_util
import utils.minikube_util


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            print('Usage: python local_deploy.py <Dockerfile path>')
            sys.exit(1)
        k8s_path = sys.argv[1]
        tagged_image = os.getenv('TAGGED_IMAGE')
        if not tagged_image:
            raise ValueError('TAGGED_IMAGE environment variable not set')
        print(f'TAGGED_IMAGE: {tagged_image}')
        utils.minikube_util.start_minikube()
        utils.minikube_util.point_docker_daemon_to_minikube()
        utils.k8s_util.setup_creds_secret()
        utils.k8s_util.k8s_apply(k8s_path, utils.constants.K8S.DEPLOYMENT_FILE)
        utils.k8s_util.k8s_apply(k8s_path, utils.constants.K8S.SERVICE_FILE)
        utils.k8s_util.k8s_apply(k8s_path, utils.constants.K8S.IGRESS_FILE)
        # expose the service
        print("Deployment ready, please expose the service to use it locally")
    except Exception as e:
        print(f"Error occurred while locally deploying the app: {e}")
        sys.exit(1)
