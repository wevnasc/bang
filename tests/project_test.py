import pytest
import os

from bang.project import (
    Field,
    Folder,
    Project,
    ProjectFactory,
    Template,
    CreateTemplateException,
    MissingFieldException
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
    project = Project(Folder(root_path), [], folders=folders)

    project.create_folders()

    assert os.listdir(tmp_folder) == ['basic']
    assert os.listdir(root_path) == ['tests', 'src']


def test_not_create_project_folders(tmp_folder):
    root_folder = os.path.join(tmp_folder, 'basic')
    project = Project(Folder(root_folder), [])
    project.create_folders()

    assert os.listdir(tmp_folder) == ['basic']
    assert os.listdir(root_folder) == []


def test_create_project_templates(template_folder, tmp_folder):
    root_folder = os.path.join(tmp_folder, 'basic')
    file_path = os.path.join(template_folder, 'default.txt')

    template = Template(file_path, 'text.txt')
    project = Project(Folder(root_folder), [template])
    project.build()

    assert os.listdir(root_folder) == ['text.txt']


def test_load_template(template_folder):
    template_text = 'template file'
    file_path = os.path.join(template_folder, 'default.txt')

    template = Template(file_path, '')

    assert template.load() == template_text


def test_create_template(template_folder, tmp_folder):
    file_path = os.path.join(template_folder, 'default.txt')

    project_folder = os.path.join(tmp_folder, 'test.txt')
    template = Template(file_path, project_folder)
    template.create()

    assert os.listdir(tmp_folder) == ['test.txt']


def test_raise_error_on_create_template(template_folder, tmp_folder):
    project_folder = os.path.join(tmp_folder, 'test/')
    template = Template('default.txt', project_folder)

    with pytest.raises(CreateTemplateException):
        template.create()


def test_load_template_and_format(template_folder):
    file_path = os.path.join(template_folder, 'params.txt')

    fields = {
        Field('name', 'basic'),
        Field('description', 'nice project'),
    }
    template = Template(file_path, '', fields)
    assert template.load() == 'my project basic nice project'


def test_load_template_wiht_many_fields(template_folder):
    file_path = os.path.join(template_folder, 'params.txt')

    fields = {
        Field('name', 'basic'),
        Field('description', 'nice project'),
        Field('version', '1.0.1')
    }
    template = Template(file_path, '', fields)
    assert template.load() == 'my project basic nice project'


def test_load_template_wiht_less_fields(template_folder):
    file_path = os.path.join(template_folder, 'params.txt')

    fields = {
        Field('name', 'basic'),
    }
    template = Template(file_path, '', fields)

    with pytest.raises(MissingFieldException):
        template.load()


def test_raise_error_when_not_is_a_valid_utf_8_file(template_folder):
    file_path = os.path.join(template_folder, 'invalid.txt')

    with pytest.raises(Exception) as error:
        template = Template('test.txt')
        template.load()
        assert error.message == 'Template file {} should be a valid utf-8 file'.format(
            file_path)


def test_define_prject_name_by_root_folder():
    project = Project(Folder('my-projects/super'), [])
    assert project.name == 'super'

    project = Project(Folder('super'), [])
    assert project.name == 'super'


def test_create_template_folder_from_dict():
    project = {
        'templates': [{"from": "text.txt", "to": "json.txt"}],
        'folders': [{"path": "src"}]
    }
    fields = [{"key": "name", "value": "value"}]
    assert isinstance(ProjectFactory.create(project, fields, 'test'), Project)
