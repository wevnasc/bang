from unittest.mock import patch
import pytest
import os

from bigbang.project import Folder, Project


def test_create_folder(temp_folder):
    folder = Folder('./tmp/tests')
    folder.create_folder()

    assert 'tests' in os.listdir(temp_folder)


@patch('bigbang.project.logger')
def test_raise_error_when_try_to_create_an_invalid_folder(logger, temp_folder):
    folder = Folder('./tmp/:')
    error_message = 'Not was possible create the folder on the directory :'

    with pytest.raises(Exception) as error:
        folder.create_folder()
        assert logger.error().assert_called_once_with(error_message)
        assert error_message == error.message


def test_create_project_folders(temp_folder):
    folders = [Folder('./tmp/tests'), Folder('./tmp/src')]
    project = Project('basic', [], folders)

    project.create_folders()

    assert 'tests' in os.listdir(temp_folder)
    assert 'src' in os.listdir(temp_folder)


def test_not_create_project_folders(temp_folder):
    project = Project('basic', [], [])
    project.create_folders()

    assert [] == os.listdir(temp_folder)
