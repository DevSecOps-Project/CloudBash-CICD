import sys

import utils.constants
import utils.executor


def k8s_apply(k8s_path, file):
    try:
        file_path = ''.join([k8s_path, file])
        cmd = [
            'kubectl',
            'apply -f',
            file_path
        ]
        output = utils.executor.execute_command(cmd)
        if ('created' in output
            or 'updated' in output
            or 'unchanged' in output):
            print('k8s file applied')
        else:
            raise Exception
    except Exception as e:
        print(f'Error occurred while applying the k8s file: {k8s_path}, {e}')
        sys.exit(1)
