import pytest
import subprocess
from unittest.mock import patch, Mock

import utils.executor


class TestExecutorUtil:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.command = []
        self.result = None

    def test_execute_command_success(self):
        self.command = ["echo", "hello"]
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "hello\n"
        mock_result.stderr = ""
        with patch('subprocess.run', return_value=mock_result):
            self.result = utils.executor.execute_command(self.command)
            assert self.result == "hello\n"

    def test_execute_command_failure(self):
        self.command = ["false"]
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "some error occurred"
        with patch('subprocess.run',
                   side_effect=subprocess.CalledProcessError(
                       returncode=1,
                       cmd=self.command,
                       output="",
                       stderr="some error occurred"
                    )
                ):
            self.result = utils.executor.execute_command(self.command)
            assert self.result == {
                'stdout': "",
                'stderr': "some error occurred",
                'returncode': 1,
                'error': 'Command \'{}\' returned with exit status 1.'.format(
                    ' '.join(self.command)
                )
            }

    def test_execute_command_unexpected_exception(self):
        self.command = ["some", "invalid", "command"]
        with patch(
            'subprocess.run',
            side_effect=Exception("unexpected error")
        ):
            self.result = utils.executor.execute_command(self.command)
            assert self.result == {
                'stdout': None,
                'stderr': None,
                'returncode': None,
                'error': "unexpected error"
            }
