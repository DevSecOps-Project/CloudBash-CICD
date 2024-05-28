import subprocess


def execute_command(command):
    try:
        cmd = ' '.join(command)
        print(f'Running command: {cmd}')
        result = subprocess.run(cmd, shell=True, check=True, text=True, capture_output=True)
        if result.returncode == 0:
            return result.stdout
        else:
            raise ValueError(
                f"command: {cmd} returned: {result.returncode} but expected 0"
                )
    except subprocess.CalledProcessError as e:
        return {
            'stdout': e.stdout,
            'stderr': e.stderr,
            'returncode': e.returncode,
            'error': str(e)
        }