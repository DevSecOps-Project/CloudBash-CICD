import sys

import utils.executor


def minikube_is_active():
    try:
        cmd = ['/opt/homebrew/bin/minikube', 'status']
        output = utils.executor.execute_command(cmd)
        active = (
            'minikube\n'
            'type: Control Plane\n'
            'host: Running\n'
            'kubelet: Running\n'
            'apiserver: Running\n'
            'kubeconfig: Configured\n\n'
        )
        if 'returncode' in output:
            if output['returncode'] == 7:
                return False
        elif output == active:
            return True
        raise Exception
    except Exception as e:
        print(f'Error occurred while checking Minikubes status: {e}')
        sys.exit(1)

def start_minikube():
    try:
        if minikube_is_active():
            print('Minikube is active')
            return
        else:
            cmd = ['/opt/homebrew/bin/minikube', 'start', '--driver=docker']
            output = utils.executor.execute_command(cmd)
            print(output)
            print('Minikube has been activated')
    except Exception as e:
        print(f'Error occurred while starting Minikube: {e}')
        sys.exit(1)

def stop_minikube():
    try:
        if minikube_is_active():
            cmd = ['/opt/homebrew/bin/minikube', 'stop', '--all']
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
        cmd = ['eval', '$(/opt/homebrew/bin/minikube -p minikube docker-env)']
        utils.executor.execute_command(cmd)
        print('Docker daemon points to Minikube')
        return
    except Exception as e:
        print(f'Error occurred while pointing Docker daemon to Minikube: {e}')
        sys.exit(1)
