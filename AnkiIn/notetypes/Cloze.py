from ..note import Note
from ..model import Model
from ..config import notetype_settings as settings
from ..log import notetype_logger as log


notetype_name = "Cloze"
if notetype_name not in settings:
    settings[notetype_name] = {}
clozeNumberPrefix = settings[notetype_name].get("clozeNumberPrefix", "[")
clozeNumberSuffix = settings[notetype_name].get("clozeNumberSuffix", "]")
priority = settings[notetype_name].get("priority", 20)


def check(lines: list) -> bool:
    return "**" in lines[0]


def get(text: str, tags: list = []) -> Note:
    sub = text.split("**")
    output = ""
    # odd indexes are clozes
    pid = 0
    for i, x in enumerate(sub):
        if(i % 2 == 1):
            id = pid + 1
            try:
                if x.startswith(clozeNumberPrefix):
                    p = x.find(clozeNumberSuffix)
                    now = x[1:p]
                    if not now.isdigit():
                        raise Exception()
                    id = int(now)
                    x = x[p + 1:]
            except Exception:
                pass
            finally:
                output = output + "{{c" + str(id) + "::" + x + "}}"
                if id == pid + 1:
                    pid = id
        else:
            output = output + x
    return ClozeNote(output, _tags=tags)


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
    def __init__(self, text, model=_model, _tags=("#Export",)):
        super().__init__(model, {"Text": text, "Back Extra": ""}, _tags)
