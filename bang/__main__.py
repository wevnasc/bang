import logging

from bang.project import ProjectFactory
from bang import cli
from bang import config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING
)


def main():

    args = cli.get_args()
    args = cli.validate_args(args)

    settings = config.load_config(args.local)
    settings = config.prefix_template(args.local, settings)

    fields = cli.ask_for_fields(settings['fields'])

    ProjectFactory.create(
        settings,
        fields,
        args.path
    ).build()


if __name__ == '__main__':
    main()
