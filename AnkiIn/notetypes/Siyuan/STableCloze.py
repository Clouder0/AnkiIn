from ..TableCloze import check as super_check
from ..TableCloze import get as super_get
from ...config import dict as conf
from ...config import config_updater
from AnkiIn.notetypes.Siyuan import SCloze


notetype_name = "STableCloze"
if notetype_name not in conf["notetype"]:
    conf["notetype"][notetype_name] = {}
settings = conf["notetype"][notetype_name]

priority = None


def update_siyuan_table_cloze_config():
    global settings, priority

    priority = settings.get("priority", 15)


config_updater.append((update_siyuan_table_cloze_config, 10))


def check(lines: list, extra_params={}) -> bool:
    return super_check(lines=lines, extra_params=extra_params)


def get(text: str, deck: str, tags: list, extra_params={}):
    return SCloze(extra_params["SiyuanID"], super_get(text=text, deck=deck, tags=tags, extra_params=extra_params))
