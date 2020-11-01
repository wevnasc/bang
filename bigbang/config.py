import json
import os
from typing import Dict


def load_config(template_folder: str) -> Dict:
    config_file = '{}/config.json'.format(template_folder)

    with open(config_file, 'r') as file:
        project_settings = json.load(file)

    return project_settings


def prefix_template(template_folder: str, settings: Dict) -> Dict:
    templates = []
    for template in settings['templates']:
        from_path = os.path.join(template_folder, template['from'])
        templates.append({**template, 'from': from_path})
    return {**settings, 'templates': templates}
