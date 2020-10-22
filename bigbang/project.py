class Field:

    def __init__(self, name: str, default_value: any = None) -> None:
        self.name = name
        self.default_value = default_value

class Folder:

    def __init__(self, name: str) -> None:
        self.name = name


class Template:

    def __init__(self, fields: list(Field)) -> None:
        self.fields = fields


class Project:

    def __init__(self, templates: list(Template), folders: list(Folder)) -> None:
        self.templates = templates
        self.folders = folders
