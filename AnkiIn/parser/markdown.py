from ..note import Note
from ..log import parser_logger as log
from ..log import notetype_logger as nlog
from ..notetype_loader import get_notetypes
from .. import config
from ..helper.formatHelper import linestrip, list2str
from enum import Enum


def get_note(text: str) -> Note:
    log.debug("Handling:%s", text)
    lines = text.splitlines(keepends=False)
    if len(lines) == 0:
        log.debug("Blank line, skipped.")
        return

    config_backup = []
    if lines[0] == "[inlineconfig]" and r"[/inlineconfig]" in lines:
        ind = lines.index(r"[/inlineconfig]")
        config_backup = config.execute_config(
            config.parse_config(list2str(lines[1:ind])))
        lines = lines[ind + 1:]
        text = list2str(lines)

    if not config.skip:
        for now in get_notetypes():
            try:
                if now.check(lines):
                    nlog.debug("Recognized as:%s", now.notetype_name)
                    return now.get(text, deck=config.deck_name, tags=config.tags)
            except Exception:
                nlog.exception("Exception Occured when handling:\n%s", text)
    log.debug("Unmatching any format")
    config_backup.reverse()
    config.execute_config(config_backup, keep_backup=False)


def handle_post(text: str):
    text = linestrip(text, left=False, right=True)
    root = build_tree(text)
    noteList = []
    dfs(root, noteList)
    return noteList


class NodeType(Enum):
    Heading = 1,
    Block = 2,


class SyntaxNode:
    def __init__(self, parent=None, value=None, type: NodeType = NodeType.Block):
        self.parent = parent
        self.sons = []
        self.value = value
        self.type = type


def build_tree(text) -> SyntaxNode:
    # Build a syntax tree for Markdown
    blocks = text.split("\n\n")
    root = SyntaxNode()
    root.value = [0, ""]
    path = [root]  # all the parents
    for x in blocks:
        if x.replace("\n", "").replace(" ", "") == "":
            continue  # skip blank block
        now = SyntaxNode()
        if x.startswith("#"):
            now.NodeType = NodeType.Heading
            level = 1
            while level < len(x) and x[level] == "#":
                level = level + 1
            now.value = [level, x[level + 1:].strip()]
            while level <= path[-1].value[0]:
                path.pop()
            now.parent = path[-1]
            path[-1].sons.append(now)
            path.append(now)
        else:
            now.NodeType = NodeType.Block
            now.value = x
            now.parent = path[-1]
            path[-1].sons.append(now)
    return root


def dfs(now: SyntaxNode, nodeList):
    config_backup = []  # save the operations for rolling back
    for x in now.sons:
        if x.NodeType is NodeType.Heading:
            dfs(x, nodeList)
        elif x.value.startswith(r"[config]"):
            config_backup += config.execute_config(config.parse_config(x.value))
        else:
            ret = get_note(x.value)
            if ret is not None:
                nodeList.append(ret)
    config_backup.reverse()
    config.execute_config(config_backup, keep_backup=False)
