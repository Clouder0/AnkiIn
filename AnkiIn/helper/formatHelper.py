import markdown2
import re
from ..config import dict as conf

# python version is 3.7, so str.removesuffix/prefix is not supported.


def remove_suffix(text: str, suffix: str) -> str:
    if not text.endswith(suffix):
        return text
    return text[:len(text) - len(suffix)]


def remove_prefix(text, prefix):
    if not text.startswith(prefix):
        return text
    return text[len(prefix):]


def markdown2html(text):
    # fix for standard markdown line-break
    # if a line is a part of a table, remove the space in the end
    text = list2str([x.rstrip() if "|" in x
                     else x.rstrip() + "  " for x in text.splitlines()])

    text = markdown2.markdown(
        text, extras=["footnotes", "tables", "task_list", "numbering", "code-friendly"])

    text = remove_suffix(remove_prefix(text, "<p>"), "</p>\n")

    return text


def linestrip(text, left=True, right=True):
    lines = text.splitlines()
    for i in range(len(lines)):
        if left:
            lines[i] = lines[i].lstrip()
        if right:
            lines[i] = lines[i].rstrip()
    return list2str(lines)


def replace_brackets(text, spliter, left, right):
    sub = text.split(spliter)
    output = ""
    flag = False
    for x in sub:
        output += left + x + right if flag else x
        flag = not flag
    return output


def list2str(target, left="", right="\n", keepsuffix=False):
    output = ""
    for x in target:
        output = output + left + x + right
    if not keepsuffix:
        output = remove_suffix(output, right)
    return output


def line_tweaks(lines: list) -> str:
    # add line-break for list and table
    inList, inTable = False, False
    text = ""
    # table start tweak. if a table starts from the first line,
    # it won"t be rendered as an empty line is added at first

    # table start
    if not inTable and "|" in lines[0] and \
            1 < len(lines) and "|" in lines[1] and "-" in lines[1]:
        text = text + "\n"
        inTable = True
    text = lines[0]

    def is_list_start(index: int) -> bool:
        return not inTable and not inList and \
            "- " not in lines[index - 1] and "- " in lines[index]

    def is_list_end(index: int) -> bool:
        return inList and "- " not in lines[index]

    def is_table_start(index: int) -> bool:
        return not inTable and "|" in lines[index] and index + 1 < len(lines)\
            and "|" in lines[index + 1] and "-" in lines[index + 1]

    def is_table_end(index: int) -> bool:
        return inTable and "|" not in lines[index]

    for i in range(1, len(lines)):
        # list start
        if is_list_start(i):
            text = text + "\n"
            inList = True
        elif is_list_end(i):
            text = text + "\n"
            inList = False
        elif is_table_start(i):
            text = text + "\n"
            inTable = True
        elif is_table_end(i):
            text = text + "\n"
            inTable = False
        text = text + "\n" + lines[i]

    return text


ESCAPE_STR = "!ESCAPER{}!"


def escape_brackets(text: str, left: str, right: str):
    recover_dict = {}
    subs = re.finditer(left + r"(.+?)" + right, text)
    result_text = ""
    id = 0
    last = 0
    for sub in subs:
        content = sub.group(1)
        escape_str = ESCAPE_STR.format(id)
        recover_dict[escape_str] = content
        id = id + 1
        result_text = result_text + text[last:sub.start()] + escape_str
        last = sub.end()
    result_text = result_text + text[last:]
    return result_text, recover_dict


def format_text(text):
    lines = text.splitlines()

    if len(lines) <= 0:
        return ""

    text = line_tweaks(lines)  # tweak for tables and lists
    if conf["mathjax"]:
        text, math_dict = escape_brackets(text, r"\$", r"\$")
    text = markdown2html(text)
    if conf["mathjax"]:
        for key, val in math_dict.items():
            text = text.replace(key, r"\({}\)".format(val))
    return text


def get_title(text: str):
    lines = text.splitlines()
    for x in lines:
        if x.startswith("# "):
            return x[2:].strip()
    return None


def is_emptytext(text: str) -> bool:
    lines = [x.strip() for x in text.splitlines()]
    for x in lines:
        if x != "":
            return False
    return True
