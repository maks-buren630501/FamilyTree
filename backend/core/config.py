import json
import os

import yaml
from pydantic.tools import lru_cache


@lru_cache
def load_config(path: str) -> dict:
    if path.split('.')[-1] == 'json':
        with open(path, 'r') as outfile:
            return json.loads(outfile.read())
    elif path.split('.')[-1] == 'yaml':
        with open(path, 'r') as outfile:
            return yaml.safe_load(outfile)


project_config = load_config(os.environ['config_path'])
