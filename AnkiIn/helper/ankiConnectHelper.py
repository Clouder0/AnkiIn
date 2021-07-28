import urllib.request
import json
from ..log import helper_logger as log


def check_online():
    try:
        get_deck_names()
    except Exception:
        log.error("Can't connect to anki-connnect.")
        return False
    return True


def request(action, **params):
    return {"action": action, "params": params, "version": 6}


def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode("utf-8")
    response = json.load(urllib.request.urlopen(
        urllib.request.Request("http://localhost:8765", requestJson)))
    if len(response) != 2:
        raise Exception("response has an unexpected number of fields")
    if "error" not in response:
        raise Exception("response is missing required error field")
    if "result" not in response:
        raise Exception("response is missing required result field")
    if response["error"] is not None:
        raise Exception(response["error"])
    return response["result"]


def add_note(target, options={"allowDuplicate": True}, retry=True):
    try:
        return invoke("addNote", note={
            "deckName": target.deck,
            "modelName": target.model.modelName,
            "fields": target.outputfields,
            "options": options,
            "tags": target.tags
        }
        )
    except Exception as e:
        if len(e.args) == 0:
            log.exception("""
                An Exception occured when adding Note:\n
                target:%s\n
                deck:%s\n
                options:%s\n
                retry:%s\n""", target.__str__(), target.deck, options.__str__(), retry)
            return
        if "model" in e.args[0] and target.model.modelName not in get_model_names_and_ids().keys():
            log.info("Model %s is not found, creating...",
                     target.model.modelName)
            create_model(target.model)
        elif "deck was not found" in e.args[0] and target.deck not in get_deck_names():
            log.info("Deck %s is not found, creating...", target.deck)
            create_deck(target.deck)
        if retry:
            return add_note(target, options, False)


def create_deck(deckName):
    return invoke("createDeck", deck=deckName)


def get_model_names_and_ids():
    return invoke("modelNamesAndIds")


def get_deck_names():
    return invoke("deckNames")


def create_model(model):
    return invoke("createModel",
                  modelName=model.modelName,
                  inOrderFields=model.fields,
                  css=model.css,
                  isCloze=model.isCloze,
                  cardTemplates=model.templates
                  )


def add_notes(notes, options={"allowDuplicate": True}):
    for x in notes:
        add_note(x, options)


def find_notes(query: str):
    return invoke("findNotes", query=query)


def update_note_fields(id: str, Note):
    invoke("updateNoteFields", note={"id": id, "fields": Note.outputfields})
