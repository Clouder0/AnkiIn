from .Cloze import get as cget
from ..config import dict as conf
from ..config import config_updater


notetype_name = "TableCloze"
if notetype_name not in conf["notetype"]:
    conf["notetype"][notetype_name] = {}
settings = conf["notetype"][notetype_name]

priority = None


def update_table_cloze_config():
    global settings, priority

    priority = settings.get("priority", 15)


config_updater.append((update_table_cloze_config, 10))


def check(lines: list, extra_params={}) -> bool:
    if len(lines) < 3:
        return False
    return "|" in lines[0] and "|" in lines[1] and "-" in lines[1] and "|" in lines[2]


def get(text: str, deck: str, tags: list, extra_params={}):
    return cget(text=text, deck=deck, tags=tags)
