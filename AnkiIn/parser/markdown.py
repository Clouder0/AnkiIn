from ..note import Note
from ..log import parser_logger as log
from ..log import notetype_logger as nlog
from .. import notetype_loader
from ..helper.formatHelper import is_emptytext
from .. import config
from ..config import dict as conf
from ..helper.formatHelper import linestrip, list2str
from enum import Enum


def get_note(text: str, extra_params={}) -> Note:
    log.debug("Handling:\n%s", text)
    lines = text.splitlines(keepends=False)
    if len(lines) == 0:
        log.debug("Blank line, skipped.")
        return

    config_backup = None
    if lines[0] == "[inlineconfig]" and r"[/inlineconfig]" in lines:
        ind = lines.index(r"[/inlineconfig]")
        config_backup = config.parse_config(list2str(lines[1:ind]))
        lines = lines[ind + 1:]
        text = list2str(lines)

    if not conf["skip"] and not is_emptytext(text):
        for now in notetype_loader.discovered_notetypes:
            try:
                if now.check(lines=lines, extra_params=extra_params):
                    nlog.debug("Recognized as:%s", now.notetype_name)
                    return now.get(text=text, deck=conf["deck_name"], tags=conf["tags"], extra_params=extra_params)
            except Exception:
                nlog.exception("Exception Occured when handling:\n%s", text)
    log.debug("Unmatching any format")

    if config_backup is not None:
        config.execute_config(config_backup)


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


def build_tree(text: str) -> SyntaxNode:
    # Build a syntax tree for Markdown
    blocks = text.split("\n\n")
    root = SyntaxNode()
    root.value = [0, ""]
    path = [root]  # all the parents
    for x in blocks:
        if x.replace("\n", "").replace(" ", "") == "":
            continue  # skip blank block
        now = SyntaxNode()
        if x.startswith("#") and x.lstrip("#")[0] == " ":
            now.NodeType = NodeType.Heading
            xx = x.split(" ")
            now.value = [len(xx[0]), xx[1]]
            while now.value[0] <= path[-1].value[0]:
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
    # save the operations for rolling back
    config_backups = []

    for x in now.sons:
        if x.NodeType is NodeType.Heading:
            dfs(x, nodeList)
        elif x.value.startswith(r"[config]"):
            config_backups.append(config.parse_config(
                list2str(x.value.splitlines()[1:])))
        else:
            ret = get_note(x.value)
            if ret is not None:
                nodeList.append(ret)

    config_backups.reverse()
    for x in config_backups:
        config.execute_config(x)
