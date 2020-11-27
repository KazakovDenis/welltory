import abc
import json
from json import JSONDecodeError
from pathlib import Path
from typing import Optional, Any

from .logger import logger


__all__ = 'validate_json_file', 'JsonContentValidator', 'validate_json_schema'

PathType = Optional[str, Path]


def read_file(filename: str) -> Optional[str]:
    """Read a file content"""
    content = None

    try:
        with open(filename) as file:
            content = file.read()
    except FileNotFoundError:
        logger.write(filename, 'No such file')

    return content


class Validator(abc.ABC):

    is_valid = False

    @abc.abstractmethod
    def validate(self, *args, **kwargs):
        """Validate an item"""


class JsonFileValidator(Validator):

    def __init__(self, filename: PathType):
        self.filename = filename
        self.raw_content = read_file(filename)
        self.valid_content = None
        self.is_valid = self.validate()

    def validate(self) -> bool:
        """Validate json file"""
        try:
            self.valid_content = json.loads(self.raw_content)
            return True
        except JSONDecodeError as e:
            msg = 'INVALID JSON. Unable to read file at position: %s' % e.pos
            logger.write(self.filename, msg)

        return False

    def get_content(self):
        """Return content if valid"""
        return self.valid_content


def validate_json_file(file_path: PathType) -> Any:
    """Check that the file is valid json"""
    return JsonFileValidator(file_path).get_content()


class JsonContentValidator(Validator):

    schema_field = 'event'

    def __init__(self, filename: str, schemas: dict):
        self.filename = filename
        self.schemas = schemas
        self.schema = None
        self.content = validate_json_file(filename)
        self.is_valid = self.validate()

    def validate(self) -> bool:
        """Check that json contains a reference to some scheme"""
        if not isinstance(self.content, dict):
            logger.write(self.filename, 'The file does not match any schema')
            return False

        self.schema = self.content.get(self.schema_field)
        if not self.schema:
            logger.write(self.filename, 'The file does not contain any schema name')
            return False

        if self.schema not in self.schemas:
            logger.write(self.filename, 'No such schema: %s' % self.schema)
            return False

        return True

    def get_content(self) -> Optional[dict]:
        """Return content if valid"""
        if self.is_valid:
            return self.content

    def get_schema(self) -> Optional[dict]:
        """Return content if valid"""
        if self.is_valid:
            return self.schema


class JsonSchemaValidator(Validator):

    def __init__(self, schema: dict, json_content: dict):
        self.schema = schema
        self.content = json_content
        self.is_valid = self.validate()

    def validate(self) -> bool:
        """Check that json contains a reference to some scheme"""


        return True


def validate_json_schema(schema: dict, filename: PathType):
    """Check that json matches the scheme"""
    return JsonSchemaValidator(schema, filename).is_valid
