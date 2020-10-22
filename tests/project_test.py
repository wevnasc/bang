import pytest
import os

from bigbang.project import Folder, CreateFolderException


def test_create_directory(temp_folder):
    folder = Folder('./tmp/tests')
    folder.create_directory()

    assert 'tests' in os.listdir(temp_folder)

def test_raise_error_when_try_to_create_an_invalid_directory(temp_folder):
    folder = Folder('./tmp/:')
    
    with pytest.raises(Exception) as error:
        folder.create_directory()
        assert 'Not was possible create the folder on the directory :' == error.message