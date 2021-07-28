from ..helper.formatHelper import list2str
from ..note import Note
from ..model import Model
from ..config import dict as conf
from ..config import config_updater
from ..log import notetype_logger as log


notetype_name = "QA"
if notetype_name not in conf["notetype"]:
    conf["notetype"][notetype_name] = {}
settings = conf["notetype"][notetype_name]

priority = None


def update_qa_config():
    global settings, priority

    priority = settings.get("priority", 10)


config_updater.append((update_qa_config, 10))


def check(lines: list, extra_params={}) -> bool:
    return len(lines) >= 2


def get(text: str, deck: str, tags: list, extra_params={}) -> Note:
    lines = text.splitlines()
    front = lines[0]
    back = list2str(lines[1:], '', '\n')
    if front == "":
        log.info("Blank front text, skipping.")
        return
    if back == "":
        log.info("Blank back text, skipping.")
        return
    return QANote(front=front, back=back, deck=deck, tags=tags)


BACK = r"""{{FrontSide}}
<hr id=answer>
{{Back}}"""

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

MODELNAME = "AnkiLink-Basic"
MODELID = 1145141921

_model = Model(
    modelId=MODELID,
    modelName=MODELNAME,
    fields=["Front", "Back"],
    templates=[
        {
            'Name': 'Card 1',
            'Front': '{{Front}}',
            'Back': BACK
        }
    ],
    css=CSS
)


class QANote(Note):
    def __init__(self, front, back, deck, tags):
        global _model
        super().__init__(model=_model, fields={
            "Front": front, "Back": back}, deck=deck, tags=tags)
