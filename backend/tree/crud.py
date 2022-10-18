from core.database.crud import Crud


class NodeCrud(Crud):

    def __init__(self):
        super().__init__("tree")
