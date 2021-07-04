from ..note import Note
from ..model import Model
from ..config import notetype_settings as settings
from ..log import notetype_logger as log
import re


notetype_name = "Cloze"
if notetype_name not in settings:
    settings[notetype_name] = {}
clozeNumberPrefix = settings[notetype_name].get("clozeNumberPrefix", r"\[")
clozeNumberSuffix = settings[notetype_name].get("clozeNumberSuffix", r"\]")
clozePrefix = settings[notetype_name].get("clozePrefix", r"\*\*")
clozeSuffix = settings[notetype_name].get("clozeSuffix", r"\*\*")
priority = settings[notetype_name].get("priority", 20)
reg = re.compile("{}({}([0-9]+?){})?(.+?){}".format(
    clozePrefix,
    clozeNumberPrefix,
    clozeNumberSuffix,
    clozeSuffix))
log.debug("Regex compiled:%s", reg.__str__())


def check(lines: list) -> bool:
    return reg.search(lines[0]) is not None


def get(text: str, deck: str = "Export", tags: list = []) -> Note:
    global reg
    subs = reg.finditer(text)
    output = ""
    # odd indexes are clozes
    pid = 0
    last = 0
    for sub in subs:
        x = sub.group(3)
        id = pid + 1 if sub.group(2) is None else sub.group(2)
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
    def __init__(self, text, model=_model, deck="Export", tags=("#Export",)):
        super().__init__(model=model, fields={
            "Text": text, "Back Extra": ""}, deck=deck, tags=tags)
