from ..helper.formatHelper import list2str
from ..note import Note
from ..config import dict as conf
from ..config import config_updater
from ..log import notetype_logger as log
from .QA import QANote


notetype_name = "MQA"
if notetype_name not in conf["notetype"]:
    conf["notetype"][notetype_name] = {}
settings = conf["notetype"][notetype_name]

priority = None
prefix = None


def update_mqa_config():
    global settings, priority, prefix

    priority = settings.get("priority", 12)
    prefix = settings.get("prefix", "!")


config_updater.append((update_mqa_config, 10))


def check(lines: list, extra_params={}) -> bool:
    return len(lines) >= 2 and len(lines[0]) >= 1 and lines[0][0] == prefix


def get(text: str, deck: str, tags: list, extra_params={}) -> Note:
    lines = text.splitlines()
    ind = 0
    while ind < len(lines) and lines[ind][0] == prefix:
        lines[ind] = lines[ind][1:]
        ind = ind + 1
    if ind == len(lines):
        log.warning("No answer is provides for MQA when handling:\n%s", text)
        return
    front = list2str(lines[:ind])
    back = list2str(lines[ind:])
    if front == "":
        log.info("Blank front text, skipping.")
        return
    if back == "":
        log.info("Blank back text, skipping.")
        return
    return QANote(front=front, back=back, deck=deck, tags=tags)
