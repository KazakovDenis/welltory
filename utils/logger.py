import logging
from pathlib import Path
from typing import Optional

import config


__all__ = 'Logger', 'logger'


class Logger:
    """Validation logger"""

    def __init__(self, name: str, file: str, fmt: Optional[str] = '%(message)s'):
        self._logger = logging.getLogger(name)
        handler = logging.FileHandler(Path().parent / file)
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.ERROR)

    def write(self, validated_file, problem):
        """Write a problem with a validated file to a log"""
        msg = 'File "%s"\n%s\n' % (validated_file, problem)
        self._logger.error(msg)


logger = Logger('json_validator', config.RESULT_FILE)
