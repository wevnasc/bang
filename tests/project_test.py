import pytest
import os

from bigbang.project import Folder, Project, LocalTemplate


def test_create_folder(temp_folder):
    folder = Folder('./tmp/tests')
    folder.create_folder()

    assert 'tests' in os.listdir(temp_folder)


def test_raise_error_when_try_to_create_an_invalid_folder(temp_folder):
    folder = Folder('./tmp/:')
    error_message = 'Not was possible create the folder on the directory :'

    with pytest.raises(Exception) as error:
        folder.create_folder()
        assert error.message == error_message


def test_create_project_folders(temp_folder):
    folders = [Folder('./tmp/tests'), Folder('./tmp/src')]
    project = Project('basic', [], folders)

    project.create_folders()

    assert 'tests' in os.listdir(temp_folder)
    assert 'src' in os.listdir(temp_folder)


def test_not_create_project_folders(temp_folder):
    project = Project('basic', [], [])
    project.create_folders()

    assert os.listdir(temp_folder) == []


def test_load_template(template_folder):
    template_text = 'template file'
    with open(os.path.join(template_folder, 'test.txt'), 'w') as file:
        file.write(template_text)

    template = LocalTemplate('test.txt')
    assert template.load() == template_text


def test_raise_error_when_not_is_a_valid_utf_8_file(template_folder):
    template_text = 'template file'.encode(encoding="ascii", errors="ignore")
    file_path = os.path.join(template_folder, 'test.txt')
    with open(file_path, 'wb') as file:
        file.write(template_text)

    with pytest.raises(Exception) as error:
        template = LocalTemplate('test.txt')
        template.load()
        assert error.message == 'Template file {} should be a valid utf-8 file'.format(
            file_path)
