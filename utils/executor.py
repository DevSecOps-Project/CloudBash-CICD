import subprocess

def execute_command(command):
    try:
        cmd = ' '.join(command)
        print(f'Running command: {cmd}')
        result = subprocess.run(cmd, shell=True, check=True, text=True, capture_output=True)
        if result.returncode == 0:
            print(f'Command succeeded with output: {result.stdout}')
            return result.stdout
        else:
            raise ValueError(f"Command '{cmd}' returned non-zero exit status {result.returncode}.")
    except subprocess.CalledProcessError as e:
        err = {
            'stdout': e.stdout,
            'stderr': e.stderr,
            'returncode': e.returncode,
            'error': f"Command '{e.cmd}' returned non-zero exit status {e.returncode}."
        }
        print(f"Command failed: {err}")
        return err
    except Exception as e:
        err = {
            'stdout': None,
            'stderr': None,
            'returncode': None,
            'error': str(e)
        }
        print(f"Unexpected error: {err}")
        return err
