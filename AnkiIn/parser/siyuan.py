from ..helper.siyuanHelper import do_property_exist_by_id, get_parent_by_id, get_property_by_id, query_sql, get_col_by_id
from . import markdown
from ..notetype_loader import discovered_notetypes
from ..notetypes.Siyuan import SQA, SMQA, SCloze, SListCloze, STableCloze
from ..config import update_config
from ..config import dict as conf
from ..config import config_updater
from .. import config


class SyntaxNode:
    def __init__(self, id: str, parent=None, sons=None):
        self.id = id
        self.parent = parent
        self.sons = sons
        if self.sons is None:
            self.sons = []


link = {}
roots = []
noteList = []
tag_attr_name = "ankilink"


def update_siyuan_parser():
    global tag_attr_name
    tag_attr_name = conf["siyuan"].get(
        "custom_attr_name", "custom-ankilink")


discovered_notetypes += [SQA, SMQA, SCloze, SListCloze, STableCloze]
config_updater.append((update_siyuan_parser, 5))
update_config()


def build_tree(now: str):
    # print("visit:{}".format(now))
    now_node = SyntaxNode(now)
    link[now] = now_node
    if do_property_exist_by_id(now, tag_attr_name):
        roots.append(now_node)
        return now_node
    fa_id = get_parent_by_id(now)
    if fa_id == "":
        return now_node
    # print("son: {} fa:{}".format(now, fa_id))
    fa = link.get(fa_id)
    if fa is None:
        fa = build_tree(fa_id)
    now_node.parent = fa
    # print("fa {} added son {}".format(fa.id, now_node.id))
    fa.sons.append(now_node)
    # print("fa {} sons:".format(fa.id))
    # print([x.id for x in fa.sons])
    return now_node


def sync(last_time: str):
    link.clear()
    roots.clear()
    noteList.clear()
    all_blocks = [x["id"] for x in query_sql(
        r"SELECT id FROM blocks where updated>'{}'".format(last_time))]
    # print(all_blocks)
    for x in all_blocks:
        build_tree(x)
    for x in roots:
        dfs(x)
    return noteList


def dfs(now: SyntaxNode):
    # print("dfs: " + now.id)
    # print([x.id for x in now.sons])
    has_config = do_property_exist_by_id(now.id, tag_attr_name)
    if has_config:
        current_config = get_property_by_id(
            now.id, tag_attr_name).replace(r"&quot;", "\"")
        config_backup = config.parse_config(current_config)
    if len(now.sons) == 0:
        # leaf
        note = markdown.get_note(get_col_by_id(
            now.id, "markdown"), extra_params={"SiyuanID": now.id})
        if note is None:
            return
        noteList.append(note)
    else:
        for x in now.sons:
            dfs(x)
    if has_config:
        config.execute_config(config_backup)
