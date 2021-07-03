from ..helper.formatHelper import list2str
from ..note import Note
from ..config import notetype_settings as settings
from ..log import notetype_logger as log
from .QA import QANote


notetype_name = "MQA"
if notetype_name not in settings:
    settings[notetype_name] = {}
priority = settings[notetype_name].get("priority", 12)


def check(lines: list) -> bool:
    return len(lines) >= 2 and lines[0][0] == "!"


def get(text: str, deck: str = "Export", tags: list = []) -> Note:
    lines = text.splitlines()
    ind = 0
    while ind < len(lines) and lines[ind][0] == "!":
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
