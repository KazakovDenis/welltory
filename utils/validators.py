import abc
import json
from json import JSONDecodeError
from pathlib import Path
from typing import Optional, Any

import jsonschema

from .logger import logger


__all__ = 'validate_json_file', 'JsonContentValidator', 'validate_json_schema'


def read_file(filename: Path) -> Optional[str]:
    """Read a file content"""
    content = None

    try:
        with open(filename) as file:
            content = file.read()
    except FileNotFoundError:
        logger.write(filename.name, 'No such file')

    return content


class Validator(abc.ABC):

    is_valid = False

    @abc.abstractmethod
    def validate(self, *args, **kwargs):
        """Validate an item"""


class JsonFileValidator(Validator):

    def __init__(self, filename: Path):
        self.filename = filename.name
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


def validate_json_file(file_path: Path) -> Any:
    """Check that the file is valid json"""
    return JsonFileValidator(file_path).get_content()


class JsonContentValidator(Validator):

    schema_field = 'event'

    def __init__(self, filename: Path, schemas: dict):
        self.filename = filename.name
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
            logger.write(self.filename, 'No such schema specified in the file: "%s"' % self.schema)
            return False

        return True

    def get_content(self) -> Optional[dict]:
        """Return content if valid"""
        if self.is_valid:
            return self.content

    def get_schema_name(self) -> Optional[str]:
        """Return content if valid"""
        return self.schema


class JsonSchemaValidator(Validator):

    def __init__(self, schema_name: str, schema: Optional[dict], filename: Path, json_content: dict):
        self.schema_name = schema_name
        self.schema = schema
        self.filename = filename.name
        self.content = json_content
        self.is_valid = self.validate()

    def validate(self) -> bool:
        """Check that the json matches the schema"""

        try:
            jsonschema.validate(self.content, self.schema)
        except jsonschema.SchemaError:
            schema_filename = self.schema_name + '.schema'
            msg = f'The schema "{self.schema_name}" does not match the global convention'
            logger.write(schema_filename, msg)
            return False
        except jsonschema.ValidationError as e:
            msg = f'The content of the file does not match the schema "{self.schema_name}": {e.message}'
            logger.write(self.filename, msg)
            return False

        return True


def validate_json_schema(schema_name: str, schema: Optional[dict], filename: Path, json_content: dict):
    """Check that json matches the schema"""
    return JsonSchemaValidator(schema_name, schema, filename, json_content).is_valid
