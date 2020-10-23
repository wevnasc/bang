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

    def __init__(self, directory: str) -> None:
        self.directory = directory

    def create_directory(self) -> None:
        try:
            if not os.path.exists(self.directory):
                os.makedirs(self.directory)
        except OSError:
            message = 'Not was possible create the folder on the directory {}'.format(self.directory)
            logging.error(message, exc_info=True)
            raise CreateFolderException(message)

    def __repr__(self) -> str:
        return '{}({})'.format(__class__, self.directory)

    def __str__(self) -> str:
        return self.directory


class Template:

    def __init__(self, fields: List[Field]) -> None:
        self.fields = fields


class Project:

    def __init__(self, templates: List[Template], folders: List[Folder]) -> None:
        self.templates = templates
        self.folders = folders
