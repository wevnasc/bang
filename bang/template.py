import glob
import json
import re
import os

from typing import List, Dict

CONFIG_FILE_NAME = "config.json"


def is_file(directory):
    return re.match(r'.+\.\w+', directory)


def list_all_directories(template_folder: str) -> List[str]:
    return glob.glob("{}/*".format(template_folder))


def remove_template_folder_prefix(
        template_folder: str,
        directories: List[str]
) -> List[str]:
    return [directory.replace('{}/'.format(template_folder), '')
            for directory in directories]


def filter_files(directories: List[str]) -> List[str]:
    return [directory for directory in directories if is_file(directory)]


def filter_folders(directories: List[str]) -> List[str]:
    return [directory for directory in directories if not is_file(directory)]


def load_config(template_folder: str) -> Dict:
    config_file = os.path.join(template_folder, CONFIG_FILE_NAME)

    with open(config_file, 'r') as file:
        project_settings = json.load(file)

    return project_settings


def remove_config_file(files):
    return [file for file in files if CONFIG_FILE_NAME not in file]
