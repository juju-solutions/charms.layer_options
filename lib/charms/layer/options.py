import os
import sys
from pathlib import Path

import yaml


_CHARM_PATH = Path(os.environ.get('JUJU_CHARM_DIR', '.'))
_DEFAULT_FILE = _CHARM_PATH / 'layer.yaml'
_CACHE = {}


def get(section=None, option=None, layer_file=_DEFAULT_FILE):
    if option and not section:
        raise ValueError('Cannot specify option without section')

    layer_file = (_CHARM_PATH / layer_file).resolve()
    if layer_file not in _CACHE:
        _CACHE[layer_file] = yaml.safe_load(layer_file.read_text())

    data = _CACHE[layer_file].get('options', {})
    if section:
        data = data.get(section, {})
    if option:
        data = data.get(option)
    return data


# terrible hack to support the old terrible interface
# try to get people to call layer.options.get() instead so
# that we can remove this garbage
# cribbed from https://stackoverflow.com/a/48100440/4941864
class BackwardsCompatibilityHack(sys.modules[__name__].__class__):
    def __call__(self, section=None, layer_file=None):
        return get(section=section,
                   layer_file=Path(layer_file or _DEFAULT_FILE))
sys.modules[__name__].__class__ = BackwardsCompatibilityHack
