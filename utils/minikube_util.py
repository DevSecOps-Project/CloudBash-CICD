import sys

import utils.executor


def minikube_is_active():
    try:
        cmd = ['minikube', 'status']
        output = utils.executor.execute_command(cmd)
        if 'returncode' in output:
            if output['returncode'] == 7:
                return False
        return True
    except Exception as e:
        print(f'Error occurred while checking Minikubes status: {e}')
        sys.exit(1)

def start_minikube():
    try:
        if minikube_is_active():
            print('Minikube is active')
            return
        else:
            cmd = ['minikube', 'start', '--driver=docker']
            output = utils.executor.execute_command(cmd)
            print(output)
            print('Minikube has been activated')
    except Exception as e:
        print(f'Error occurred while starting Minikube: {e}')
        sys.exit(1)

def stop_minikube():
    try:
        if minikube_is_active():
            cmd = ['minikube', 'stop', '--all']
            output = utils.executor.execute_command(cmd)
            print(output)
            print('Minikube has been stopped')
            return
        else:
            print('Minikube is off')
            return
    except Exception as e:
        print(f'Error occurred while stopping Minikube: {e}')
        sys.exit(1)

def point_docker_daemon_to_minikube():
    try:
        cmd = ['eval', '$(minikube -p minikube docker-env)']
        utils.executor.execute_command(cmd)
        print('Docker daemon points to Minikube')
        return
    except Exception as e:
        print(f'Error occurred while pointing Docker daemon to Minikube: {e}')
        sys.exit(1)
