import os
import logging
from typing import List

logger = logging.getLogger(__name__)


class CreateFolderException(Exception):
    def __init__(self, message):
        super(CreateFolderException, self).__init__(message)


class Field:

    def __init__(self, name: str, default_value: any = None) -> None:
        self.name = name
        self.default_value = default_value


class Folder:

    def __init__(self, path: str) -> None:
        self.path = path

    def create_folder(self) -> None:
        try:
            if not os.path.exists(self.path):
                os.makedirs(self.path)
        except OSError:
            message = 'Not was possible create the folder on the directory {}'.format(
                self.path)
            logger.error(message, exc_info=True)
            raise CreateFolderException(message)

    def __repr__(self) -> str:
        return '{}({})'.format(__class__, self.path)

    def __str__(self) -> str:
        return self.path


class Template:

    def __init__(self, fields: List[Field]) -> None:
        self.fields = fields


class Project:

    def __init__(self, name: str, templates: List[Template], folders: List[Folder]) -> None:
        self.name = name
        self.templates = templates
        self.folders = folders

    def create_folders(self):
        for directory in self.folders:
            directory.create_folder()
        logger.info('{} project folders created'.format(self.name))

    def __repr__(self) -> str:
        return '{}({}, {})'.format(__class__, self.name, self.templates, self.folders)

    def __str__(self) -> str:
        return self.name
