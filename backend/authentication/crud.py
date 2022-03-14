from backend.core.database.crud import BaseCrud


class UserCrud(BaseCrud):

    def __init__(self):
        super().__init__("users")
