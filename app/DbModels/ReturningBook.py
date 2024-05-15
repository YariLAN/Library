class ReturningBook:
    __tableName__ = "returning_books"

    def __init__(self, librarian_id: int, issued_book_id: int, date_of_actual: str):
        self.librarian_id = librarian_id
        self.issued_book_id = issued_book_id
        self.date_of_actual = date_of_actual
        