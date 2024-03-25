import sys
import yaml
import os.path as path
from enum import Enum, auto
from typing import NoReturn

# Create this file and start putting values in there if you wanna change shit
CONFIG_FNAME = 'codegen.yaml'

class ConfigField(Enum):
    use_cloc = auto()
    cloc_executable = auto()
    python_executable = auto()

DEFAULTS = {
    ConfigField.use_cloc: False,
    ConfigField.cloc_executable: 'cloc',
    ConfigField.python_executable: 'python'
}

def panic(msg: str) -> NoReturn:
    print(f'CONFIG ERROR: {msg}')
    sys.exit()

def get_config(key: ConfigField) -> str:
    if path.exists(CONFIG_FNAME):
        with open(CONFIG_FNAME, 'rt') as fh:
            values = yaml.safe_load(fh)
        if key.name in values:
            return values[key.name]
    
    if key in DEFAULTS: return str(DEFAULTS[key])

    panic(f'Key {key} not found in values file or DEFAULTS')