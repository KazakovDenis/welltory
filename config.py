import os
from pathlib import Path


EVENT_SRC = Path('task_folder', 'event').absolute()
SCHEMA_SRC = Path('task_folder', 'schema').absolute()

events = os.listdir(EVENT_SRC)
schemas = os.listdir(SCHEMA_SRC)
