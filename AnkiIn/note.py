from .helper.formatHelper import format_text


class Note:
    def __init__(self, model, fields={}, deck="Export", tags=[]):
        self.model = model
        self.fields = fields
        self.outputfields = self.fields.copy()
        for x in self.outputfields.keys():
            self.outputfields[x] = format_text(self.outputfields[x])
        self.deck = deck
        self.tags = tags

    def __getitem__(self, key):
        if key not in self.fields:
            raise KeyError
        return self.fields[key]

    def __setitem__(self, key, value):
        self.fields[key] = value
        self.outputfields[key] = format_text(value)
