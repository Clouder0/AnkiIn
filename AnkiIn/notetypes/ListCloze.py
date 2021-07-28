from .Cloze import get as cget
from ..config import dict as conf
from ..config import config_updater


notetype_name = "ListCloze"
if notetype_name not in conf["notetype"]:
    conf["notetype"][notetype_name] = {}
settings = conf["notetype"][notetype_name]

priority = None


def update_list_cloze_config():
    global settings, priority

    priority = settings.get("priority", 10)


config_updater.append((update_list_cloze_config, 10))


def check(lines: list, extra_params={}) -> bool:
    return lines[0].startswith("- ")


def get(text: str, deck: str, tags: list, extra_params={}):
    return cget(text=text, deck=deck, tags=tags)
