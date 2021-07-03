from collections import defaultdict
import genanki
import hashlib


def get_note(mynote):
    return genanki.Note(
        model=get_model(mynote.model),
        fields=list(mynote.outputfields.values()),
        tags=mynote.tags)


def get_model(mymodel):
    return genanki.Model(
        model_id=mymodel.modelId,
        name="G" + mymodel.modelName,  # avoid duplicating
        fields=list([{"name": x} for x in mymodel.fields]),
        templates=[{"name": x["Name"], "qfmt":x["Front"], "afmt":x["Back"]}
                   for x in mymodel.templates],
        model_type=mymodel.isCloze,
        css=mymodel.css
    )


def get_id_from_str(text):
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest(), 16) % 10**10


def get_deck(deckname: str):
    return genanki.Deck(get_id_from_str(deckname), deckname)


def generate_deck(deckname: str, note_list: list):
    deck = get_deck(deckname)
    for x in note_list:
        deck.add_note(get_note(x))
    return deck


def get_package(note_list: list):
    deck_sort = defaultdict(list)
    for x in note_list:
        deck_sort[x.deck].append(x)
    decks = []
    for x in deck_sort.keys():
        decks.append(generate_deck(x, deck_sort[x]))
    return genanki.Package(decks)


def export_notes(note_list: list, path: str):
    get_package(note_list).write_to_file(path)
