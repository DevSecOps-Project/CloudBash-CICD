import subprocess


def execute_command(command):
    try:
        cmd = ' '.join(command)
        print(f'Running command: {cmd}')
        result = subprocess.run(cmd, shell=True, check=True, text=True, capture_output=True)
        if result.returncode == 0:
            print("inside if")
            return result.stdout
        raise ValueError(
            f"command: {cmd} returned: {result.returncode} but expected 0"
        )
    except subprocess.CalledProcessError as e:
        return {
            'stdout': e.output,
            'stderr': e.stderr,
            'returncode': e.returncode,
            'error': f"Command '{e.cmd}' returned non-zero exit status {e.returncode}."
        }
    except Exception as e:
        return {
            'stdout': None,
            'stderr': None,
            'returncode': None,
            'error': str(e)
        }
