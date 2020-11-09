import logging

from bang.project import ProjectFactory
from bang import cli
from bang import template

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING
)


def main():
    args = cli.get_args()
    args = cli.validate_args(args)

    directories = template.list_all_directories(args.local)
    directories = template.remove_template_folder_prefix(
        args.local,
        directories
    )

    config = template.load_config(args.local)

    folders = template.filter_folders(directories)
    templates = template.filter_files(directories)
    templates = template.remove_config_file(templates)
    fields = cli.ask_for_fields(config['fields'])

    ProjectFactory.create(
        args.local,
        args.path,
        folders,
        templates,
        fields
    ).build()


if __name__ == '__main__':
    main()
