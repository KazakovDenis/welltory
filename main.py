from pathlib import Path
from typing import Dict, Optional

import config
from utils import *


def get_schemas(source: Path) -> Dict[str, Optional[dict]]:
    """Read and save schemas"""
    schema_cache = {}
    ext = '.schema'

    for filename in config.schemas:
        if filename.endswith(ext):
            schema_name = filename.rsplit(ext, maxsplit=1)[0]
            schema = validate_json_file(source / filename)
            schema_cache[schema_name] = schema
            if not isinstance(schema, dict):
                msg = 'BAD SCHEMA. A JSON schema must be of type "dict" (Python) / "object" (Javascript)'
                logger.write(filename, msg)

    return schema_cache


def main():
    """Start validating"""
    schema_cache = get_schemas(config.SCHEMA_SRC)

    for filename in config.events:
        validator = JsonContentValidator(filename, schema_cache)
        valid_content = validator.get_content()

        if valid_content:
            schema_name = validator.get_schema_name()
            schema = schema_cache.get(schema_name)
            if schema:
                validate_json_schema(schema_name, schema, filename, valid_content)

    print('Check the results in %s' % config.RESULT_FILE)


if __name__ == '__main__':
    main()
