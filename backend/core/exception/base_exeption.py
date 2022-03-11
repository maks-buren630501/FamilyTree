class UniqueIndexException(Exception):
    """Обработка занесения значения в базу данных уникального значения"""

    def __init__(self, detail: dict, message: str = "Ошибка проверки уникальности поля"):
        self.message = message
        self.detail = detail
        super().__init__(self.detail, self.message)
