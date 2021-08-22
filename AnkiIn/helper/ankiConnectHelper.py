import json
from ..log import helper_logger as log
import asyncio
import aiohttp


async def check_online():
    try:
        await get_deck_names()
    except Exception:
        log.error("Can't connect to anki-connnect.")
        return False
    return True


def request(action, **params):
    return {"action": action, "params": params, "version": 6}


async def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode("utf-8")
    async with aiohttp.ClientSession() as session:
        async with session.post("http://localhost:8765", data=requestJson) as resp:
            response = json.loads(await resp.text())
            if len(response) != 2:
                raise Exception("response has an unexpected number of fields")
            if "error" not in response:
                raise Exception("response is missing required error field")
            if "result" not in response:
                raise Exception("response is missing required result field")
            if response["error"] is not None:
                raise Exception(response["error"])
            return response["result"]


async def add_note(target, options={"allowDuplicate": True}, retry=True):
    try:
        return await invoke("addNote", note={
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
        if "model" in e.args[0] and target.model.modelName not in (await get_model_names_and_ids()).keys():
            log.info("Model %s is not found, creating...",
                     target.model.modelName)
            await create_model(target.model)
        elif "deck was not found" in e.args[0] and target.deck not in (await get_deck_names()):
            log.info("Deck %s is not found, creating...", target.deck)
            await create_deck(target.deck)
        if retry:
            return await add_note(target, options, False)


async def create_deck(deckName):
    return await invoke("createDeck", deck=deckName)


async def get_model_names_and_ids():
    return await invoke("modelNamesAndIds")


async def get_deck_names():
    return await invoke("deckNames")


async def create_model(model):
    return await invoke("createModel",
                        modelName=model.modelName,
                        inOrderFields=model.fields,
                        css=model.css,
                        isCloze=model.isCloze,
                        cardTemplates=model.templates
                        )


async def add_notes(notes, options={"allowDuplicate": True}):
    for x in notes:
        await add_note(x, options)


async def find_notes(query: str):
    return await invoke("findNotes", query=query)


async def update_note_fields(id: str, Note):
    await invoke("updateNoteFields", note={"id": id, "fields": Note.outputfields})
