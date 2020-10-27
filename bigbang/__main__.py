import logging
import os
import json

from bigbang.project import ProjectFactory, BASE_DIR

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)


def main():
    with open(os.path.join(BASE_DIR, 'templates/config.json'), 'r') as file:
        dict_project = json.load(file)
        project = ProjectFactory.create_from_dict(
            dict_project, os.path.join(BASE_DIR, 'spacebot'))
        project.create_folders()
        project.create_templates()


if __name__ == '__main__':
    main()
