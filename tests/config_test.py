from tests.conftest import template_folder
from bang import config


def test_should_load_config_file_as_dict(template_folder):
    loaded_config = config.load_config(template_folder)

    expected_config = {
        "fields": [{"key": "description"}],
        "folders": [{"path": "src"}, {"path": "test"}],
        "templates": [{"from": "README.md", "to": "README.md"}, {"from": "empty.txt", "to": "src/index.js"}]
    }

    assert loaded_config == expected_config

def test_should_prefix_template_with_template_folder(template_folder):
  test_config = config.load_config(template_folder)
  test_config = config.prefix_template(template_folder, test_config)

  for template in test_config['templates']:
    assert template_folder in template['from']