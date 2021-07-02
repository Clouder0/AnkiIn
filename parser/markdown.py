from ..note import Note
from ..log import parser_logger as log
from ..log import notetype_logger as nlog
from ..notetype_loader import get_notetypes
from .. import config
from ..helper.formatHelper import linestrip


def get_note(text: str) -> Note:
    log.debug("Handling:%s", text)
    lines = text.splitlines(keepends=False)
    if len(lines) == 0:
        log.debug("Blank line, skipped.")
        return
    for now in get_notetypes():
        try:
            if now.check(lines):
                nlog.debug("Recognized as:%s", text,
                           now.__name__.split(".")[-1])
                return now.get(text, tags=config.tags)
        except Exception:
            nlog.exception("Exception Occured when handling:\n%s", text)
    log.debug("Unmatching any format", text)


def handle_post(text: str):
    text = linestrip(text, left=False, right=True)
    notes = text.split("\n\n")
    noteList = []
    for note in notes:
        noteList.append(get_note(note))
    return noteList
