from .helper import genankiHelper


class Model:
    def __init__(self, modelName: str, css: str, modelId: str = None,
                 fields: list = [], templates: list = [], isCloze: int = 0):
        self.modelName = modelName
        if modelId is None:
            self.modelId = genankiHelper.get_id_from_str(modelName)
        else:
            self.modelId = modelId
        self.fields = fields
        self.templates = templates
        self.isCloze = isCloze
        self.css = css
