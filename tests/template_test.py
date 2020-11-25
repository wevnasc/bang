import os
from bang import template


def test_should_load_config_file_as_dict(template_folder):
    loaded_config = template.load_config(template_folder)

    expected_config = {
        "fields": [{"key": "description"}]
    }

    assert loaded_config == expected_config


def test_is_file():
    assert not template.is_file('test')
    assert not template.is_file('test/config')
    assert template.is_file('test.json')
    assert template.is_file('test/test.py')
    assert template.is_file('test.c')


def test_list_add_directories(template_folder):
    assert template.list_all_directories(template_folder) == [
        os.path.join(template_folder, 'config.json'),
        os.path.join(template_folder, 'params.txt'),
        os.path.join(template_folder, 'default.txt'),
        os.path.join(template_folder, 'invalid.txt'),
    ]


def test_filter_folders():
    assert template.filter_folders(['tests', 'tests/test.js']) == ['tests']


def test_filter_files():
    assert template.filter_files(['tests', 'tests/test.js']) == ['tests/test.js']


def test_remove_config_file():
    assert template.remove_config_file(['tests/test.js', 'tests/config.json']) == ['tests/test.js']
