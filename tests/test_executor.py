import subprocess
from unittest.mock import patch, Mock

import pytest

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
        with patch('subprocess.run',
                   side_effect=subprocess.CalledProcessError(
                       returncode=1,
                       cmd=' '.join(self.command),
                       output="",
                       stderr="some error occurred"
                    )
                ):
            self.result = utils.executor.execute_command(self.command)
            assert self.result == {
                'stdout': "",
                'stderr': "some error occurred",
                'returncode': 1,
                'error': "Command 'false' returned non-zero exit status 1."
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
