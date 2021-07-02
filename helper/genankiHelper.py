import genanki
import hashlib


def get_note(mynote):
    return genanki.Note(model=get_model(mynote.model), fields=list(mynote.outputfields.values()), tags=mynote.tags)


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


def get_deck(deckname, notes):
    deck = genanki.Deck(get_id_from_str(deckname), deckname)
    for x in notes:
        deck.add_note(get_note(x))
    return deck


def export_deck(deck, path):
    genanki.Package(deck).write_to_file(path)
