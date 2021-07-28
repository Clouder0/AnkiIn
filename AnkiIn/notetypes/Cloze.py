from ..note import Note
from ..model import Model
from ..config import dict as conf
from ..config import config_updater
from ..log import notetype_logger as log
import re


notetype_name = "Cloze"
if notetype_name not in conf["notetype"]:
    conf["notetype"][notetype_name] = {}
settings = conf["notetype"][notetype_name]

clozeNumberPrefix = None
clozeNumberSuffix = None
clozePrefix = None
clozeSuffix = None
priority = None
reg = None


def update_cloze_config():
    global settings, clozeNumberPrefix, clozeNumberSuffix, clozePrefix, clozeSuffix, priority, reg

    clozeNumberPrefix = settings.get("clozeNumberPrefix", r"\[")
    clozeNumberSuffix = settings.get("clozeNumberSuffix", r"\]")
    clozePrefix = settings.get("clozePrefix", r"\*\*")
    clozeSuffix = settings.get("clozeSuffix", r"\*\*")
    priority = settings.get("priority", 20)
    reg = re.compile("{}({}([0-9]+?){})?(.+?){}".format(
        clozePrefix,
        clozeNumberPrefix,
        clozeNumberSuffix,
        clozeSuffix))

    log.debug("Regex compiled:%s", reg.__str__())


config_updater.append((update_cloze_config, 10))


def check(lines: list, extra_params={}) -> bool:
    return reg.search(lines[0]) is not None


def get(text: str, deck: str, tags: list, extra_params={}) -> Note:
    global reg
    subs = reg.finditer(text)
    output = ""
    # odd indexes are clozes
    pid = 0
    last = 0
    for sub in subs:
        x = sub.group(3)
        id = pid + 1 if sub.group(2) is None else sub.group(2)
        id = int(id)
        log.debug("Cloze:\n%s\nid:%d", x, id)
        output = output + text[last:sub.start()] + "{{c" + str(id) + "::" + x + "}}"
        last = sub.end()
        if id == pid + 1:
            pid = id
    output = output + text[last:]
    return ClozeNote(text=output, deck=deck, tags=tags)


CSS = r""".card {
  font-family: arial;
  font-size: 20px;
  text-align: center;
  color: black;
  background-color: white;
}

.cloze {
 font-weight: bold;
 color: blue;
}
.nightMode .cloze {
 color: lightblue;
}
ul {
display: inline-block;
text-align: left;
}
ol {
display: inline-block;
text-align: left;
}
"""

MODELNAME = "AnkiLink-Cloze"
MODELID = 1145141920

_model = Model(
    modelId=MODELID,
    modelName=MODELNAME,
    isCloze=1,
    fields=["Text", "Back Extra"],
    templates=[
        {
            "Name": "Cloze",
            "Front": "{{cloze:Text}}",
            "Back": "{{cloze:Text}}",
        }
    ],
    css=CSS
)


class ClozeNote(Note):
    def __init__(self, text, deck, tags):
        global _model
        super().__init__(model=_model, fields={
            "Text": text, "Back Extra": ""}, deck=deck, tags=tags)
