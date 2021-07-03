from ..helper.formatHelper import list2str
from ..note import Note
from ..model import Model
from ..config import notetype_settings as settings
from ..log import notetype_logger as log


notetype_name = "Choices"
if notetype_name not in settings:
    settings[notetype_name] = {}
priority = settings[notetype_name].get("priority", 10)


def check(lines: list) -> bool:
    return len(lines) >= 2


def get(text: str, deck: str = "Export", tags: list = []) -> Note:
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
    def __init__(self, front, back, model=_model, deck="Export", tags=("#Export",)):
        super().__init__(model=model, fields={
            "Front": front, "Back": back}, deck=deck, tags=tags)
