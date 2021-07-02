from .helper import genankiHelper


class Model:
    def __init__(self, modelName, css, modelId=None, fields=[], templates=[], isCloze=0):
        self.modelName = modelName
        if modelId is None:
            self.modelId = genankiHelper.get_id_from_str(modelName)
        else:
            self.modelId = modelId
        self.fields = fields
        self.templates = templates
        self.isCloze = isCloze
        self.css = css
