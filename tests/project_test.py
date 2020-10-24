import pytest
import os

from bigbang.project import (
    Field,
    Folder,
    Project,
    LocalTemplate
)


def test_create_folder(tmp_folder):
    folder = Folder('./tmp/tests')
    folder.create_folder()

    assert 'tests' in os.listdir(tmp_folder)


def test_create_sub_folder(tmp_folder):
    root_folder = './tmp/tests'
    folder = Folder(root_folder)
    folder.add_sub_folder(Folder('config'))
    folder.create_folder()

    assert os.listdir(tmp_folder) == ['tests']
    assert os.listdir(root_folder) == ['config']


def test_raise_error_when_try_to_create_an_invalid_folder(tmp_folder):
    folder = Folder('./tmp/:')
    error_message = 'Not was possible create the folder on the directory :'

    with pytest.raises(Exception) as error:
        folder.create_folder()
        assert error.message == error_message


def test_create_project_folders(tmp_folder):
    root_path = os.path.join(tmp_folder, 'basic')
    folders = [Folder('tests'), Folder('src')]
    project = Project('basic', Folder(root_path), folders)

    project.create_folders()

    assert os.listdir(tmp_folder) == ['basic']
    assert os.listdir(root_path) == ['tests', 'src']


def test_not_create_project_folders(tmp_folder):
    root_folder = os.path.join(tmp_folder, 'basic')
    project = Project('basic', Folder(root_folder), [])
    project.create_folders()

    assert os.listdir(tmp_folder) == ['basic']
    assert os.listdir(root_folder) == []


def test_load_template(template_folder):
    template_text = 'template file'
    with open(os.path.join(template_folder, 'test.txt'), 'w') as file:
        file.write(template_text)

    template = LocalTemplate('test.txt')
    assert template.load() == template_text


def test_load_template_and_format(template_folder):
    template_text = 'my project {name} {description}'
    with open(os.path.join(template_folder, 'test.txt'), 'w') as file:
        file.write(template_text)

    name_field = Field('name', 'basic')
    description_field = Field('description', 'nice project')
    template = LocalTemplate('test.txt', [name_field, description_field])
    assert template.load() == 'my project basic nice project'


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
