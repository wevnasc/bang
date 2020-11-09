import os
import logging
from typing import Any, List, Set, Dict
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
            key: str,
            value: str,
            default_value: Any = None
    ) -> None:
        self.key = key
        self.value = value
        self.default_value = default_value

    def __eq__(self, o: Any) -> bool:
        return self.key == o.key

    def __hash__(self):
        return hash(self.key)

    def __repr__(self) -> str:
        return '{}({}, {}, {})'.format(
            self.__class__,
            self.key,
            self.value,
            self.default_value
        )

    def __str__(self) -> str:
        return self.key


class Template:

    def __init__(
            self,
            from_path: str,
            to_path: str,
            fields: Set[Field] = None
    ) -> None:
        self.from_path = os.path.join(BASE_DIR, from_path)
        self.to_path = to_path
        self.fields = fields if fields is not None else set()
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
                lambda data, field: {**data, field.key: field.value},
                self.fields, {}
            )
            return content.format(**fields)
        except KeyError as error:
            message = 'Field {} not found'.format(error)
            logger.error(message, exc_info=True)
            raise MissingFieldException(message)

    def __repr__(self) -> str:
        return '{}({}, {}, {})'.format(
            self.__class__,
            self.from_path,
            self.to_path,
            self.fields
        )


class Folder:

    def __init__(self, path: str) -> None:
        self.path = path
        self.sub_folders: List[Folder] = []

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
        return '{}({})'.format(self.__class__, self.path)

    def __str__(self) -> str:
        return self.path


class Project:

    def __init__(
            self,
            root_folder: Folder,
            templates: List[Template],
            folders: List[Folder] = None,
    ) -> None:
        self.root_folder = root_folder
        self.folders = folders if folders is not None else []
        self.templates = templates

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
            template.fields.add(self._field_name())
            template.create()

        logger.info('{} templates created'.format(self.name))

    def build(self):
        self.create_folders()
        self.create_templates()

    def _field_name(self) -> Field:
        return Field('name', self.name)

    def __repr__(self) -> str:
        return '{}({}, {}, {})'.format(
            self.__class__,
            self.root_folder,
            self.templates,
            self.folders,
        )

    def __str__(self) -> str:
        return self.name


class ProjectFactory:

    @staticmethod
    def create(
            template_folder: str,
            project_folder: str,
            folders: List[str],
            templates: List[str],
            fields: List[Dict]
    ):
        project_folders: List[Folder] = [Folder(folder) for folder in folders]
        template_fields: Set[Field] = set(Field(**field) for field in fields)

        project_templates: List[Template] = [Template(
            from_path=os.path.join(template_folder, template),
            to_path=os.path.join(project_folder, template),
            fields=template_fields
        ) for template in templates]

        return Project(
            Folder(project_folder),
            project_templates,
            project_folders
        )
