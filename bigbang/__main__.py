import logging
import os

from bigbang.project import (
    Field,
    Folder,
    Project,
    Template,
    BASE_DIR
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)


def main():
    fields = {Field('project', 'startup'), Field(
        'name', 'Weverson Nascimento')}
    templates = [
        Template(os.path.join(BASE_DIR, 'templates/' 'README.md'), 'README.md')
    ]
    project = Project(Folder(os.path.join(BASE_DIR, 'startup')),
                      templates, fields=fields)
    project.create_folders()
    project.create_templates()


if __name__ == '__main__':
    main()
