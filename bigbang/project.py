import os
import logging
from typing import List, Set
from functools import reduce

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class CreateFolderException(Exception):
    def __init__(self, message):
        super(CreateFolderException, self).__init__(message)


class CreateTemplateException(Exception):
    def __init__(self, message):
        super(CreateTemplateException, self).__init__(message)


class MissingFieldException(Exception):
    def __init__(self, message):
        super(MissingFieldException, self).__init__(message)


class Field:

    def __init__(
        self,
        name: str,
        value: str,
        default_value: any = None
    ) -> None:
        self.name = name
        self.value = value
        self.default_value = default_value

    def __eq__(self, o: object) -> bool:
        return self.name == o.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self) -> str:
        return '{}({}, {}, {})'.format(
            __class__,
            self.name,
            self.value,
            self.default_value
        )

    def __str__(self) -> str:
        return self.name


class Template:

    def __init__(
        self,
        from_path: str,
        to_path: str,
        fields: Set[Field] = None
    ) -> None:
        self.from_path = os.path.join(BASE_DIR, from_path)
        self.to_path = to_path
        self.fields = fields if fields is not None else []
        self._content = None

    def load(self):
        try:
            with open(self.from_path, 'r') as file:
                self._content = file.read()
            return self._load_fields(self._content)
        except UnicodeDecodeError:
            message = 'Template file {} should be a valid utf-8 file'.format(
                self.from_path)
            logger.error(message, exc_info=True)
            raise ValueError(message)

    def create(self):
        try:
            with open(self.to_path, 'w') as file:
                file.write(self.load())
        except OSError:
            message = 'Not was possible create template {}'.format(
                self.to_path)
            logger.error(message, exc_info=True)
            raise CreateTemplateException(message)

    def _load_fields(self, content):
        try:
            fields = reduce(
                lambda dict, field: {**dict, field.name: field.value},
                self.fields, {}
            )
            return content.format(**fields)
        except KeyError as error:
            message = 'Field {} not found'.format(error)
            logger.error(message, exc_info=True)
            raise MissingFieldException(message)


class Folder:

    def __init__(self, path: str) -> None:
        self.path = path
        self.sub_folders = []

    def add_sub_folder(self, folder):
        folder.path = os.path.join(self.path, folder.path)
        self.sub_folders.append(folder)

    def create_folder(self) -> None:
        try:
            if not os.path.exists(self.path):
                os.makedirs(self.path)
        except OSError:
            message = 'Not was possible create the folder {}'.format(
                self.path)
            logger.error(message, exc_info=True)
            raise CreateFolderException(message)

        self._create_sub_folders()

    def _create_sub_folders(self) -> None:
        for folder in self.sub_folders:
            folder.create_folder()

    def __repr__(self) -> str:
        return '{}({})'.format(__class__, self.path)

    def __str__(self) -> str:
        return self.path


class Project:

    def __init__(
        self,
        root_folder: Folder,
        templates: List[Template],
        folders: List[Folder] = None,
        fields: Set[Field] = None
    ) -> None:
        self.root_folder = root_folder
        self.folders = folders if folders is not None else []
        self.templates = self._add_templates_to_project(templates)
        self.fields = fields if fields is not None else []

    @property
    def name(self):
        return self.root_folder.path.split('/')[-1]

    def create_folders(self):
        for folder in self.folders:
            self.root_folder.add_sub_folder(folder)
        self.root_folder.create_folder()

        logger.info('{} project folders created'.format(self.name))

    def create_templates(self):
        for template in self.templates:
            template.fields = self.fields
            template.create()

        logger.info('{} templates created'.format(self.name))

    def _add_templates_to_project(self, templates):
        for template in templates:
            template.to_path = os.path.join(
                self.root_folder.path, template.to_path)
        return templates

    def __repr__(self) -> str:
        return '{}({}, {}, {}, {})'.format(
            __class__,
            self.root_folder,
            self.templates,
            self.folders,
            self.fields
        )

    def __str__(self) -> str:
        return self.name
