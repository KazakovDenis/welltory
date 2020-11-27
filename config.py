import os
from pathlib import Path


RESULT_FILE = 'result.log'
EVENT_SRC = Path('task_folder', 'event').absolute()
SCHEMA_SRC = Path('task_folder', 'schema').absolute()

events = [EVENT_SRC / file for file in os.listdir(EVENT_SRC)]
schemas = os.listdir(SCHEMA_SRC)
