from ...note import Note
from ..QA import get as super_get
from ...model import Model
from ...config import dict as conf
from ...config import config_updater


notetype_name = "SQA"
if notetype_name not in conf["notetype"]:
    conf["notetype"][notetype_name] = {}
settings = conf["notetype"][notetype_name]

priority = None


def update_sqa_config():
    global settings, priority

    priority = settings.get("priority", 11)


config_updater.append((update_sqa_config, 10))


def check(lines: list) -> bool:
    return len(lines) >= 2


def get(text: str, deck: str = "Export", tags: list = [], SiyuanID: str = "") -> Note:
    res = super_get(text, deck, tags)
    res.fields["SiyuanID"] = SiyuanID
    res.model = _model
    return res


BACK = r"""{{FrontSide}}
<hr id=answer>
{{Back}}
</br>
<a href="siyuan://blocks/{{SiyuanID}}">Open in SiYuan</a>"""

CSS = r""".card {
  font-family: arial;
  font-size: 20px;
  text-align: center;
  color: black;
  background-color: white;
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

MODELNAME = "SAnkiLink-Basic"
MODELID = 1145841921

_model = Model(
    modelId=MODELID,
    modelName=MODELNAME,
    fields=["Front", "Back", "SiyuanID"],
    templates=[
        {
            'Name': 'Card 1',
            'Front': '{{Front}}',
            'Back': BACK
        }
    ],
    css=CSS
)
