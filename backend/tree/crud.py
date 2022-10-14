from core.database.crud import BaseCrud


class NodeCrud(BaseCrud):

    def __init__(self):
        super().__init__("tree")
