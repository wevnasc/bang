from unittest.mock import patch
import pytest
import os

from bigbang.project import Folder


def test_create_directory(temp_folder):
    folder = Folder('./tmp/tests')
    folder.create_directory()

    assert 'tests' in os.listdir(temp_folder)

@patch('bigbang.project.logger')
def test_raise_error_when_try_to_create_an_invalid_directory(logger, temp_folder):
    folder = Folder('./tmp/:')
    error_message = 'Not was possible create the folder on the directory :'
    
    with pytest.raises(Exception) as error:
        folder.create_directory()
        assert logger.error().assert_called_once_with(error_message)
        assert error_message == error.message