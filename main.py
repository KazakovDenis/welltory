import os
from pathlib import Path
from typing import Dict, Optional

from utils import *


EVENT_SRC = Path('task_folder', 'event').absolute()
SCHEMA_SRC = Path('task_folder', 'schema').absolute()

events = os.listdir(EVENT_SRC)
schemas = os.listdir(SCHEMA_SRC)


def get_schemas(source: Path) -> Dict[str, Optional[str]]:
    """Read and save schemas"""
    schema_cache = {}

    for filename in schemas:
        if filename.endswith('.schema'):
            schema_name = filename.rsplit('.schema', maxsplit=1)[0]
            schema = validate_json_file(source / filename)
            schema_cache[schema_name] = schema
            if not isinstance(schema, dict):
                logger.write(filename, 'BAD SCHEMA')

    return schema_cache


def main():
    """Start validating"""
    schema_cache = get_schemas(SCHEMA_SRC)

    for filename in events:
        validator = JsonContentValidator(EVENT_SRC / filename, schema_cache)
        valid_content = validator.get_content()
        if valid_content:
            schema = validator.get_schema()
            validate_json_schema(schema, valid_content)


if __name__ == '__main__':
    main()
