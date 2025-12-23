from .collections import BookCollection, IndexDict

class Library:
    def __init__(self):
        self.books = BookCollection()
        self.index = IndexDict()

    def add_book(self, book):
        self.books.add(book)
        self.index[book.isbn] = book
        print(f"Добавлена книга: {book}")

    def remove_book(self, isbn):
        book = self.index[isbn]
        if book:
            self.books.remove(book)
            del self.index[isbn]
            print(f"Удалена книга: {book}")

    def find_by_author(self, author):
        return self.index.get_by_author(author)

    def find_by_year(self, year):
        return self.index.get_by_year(year)

    def find_by_isbn(self, isbn):
        return self.index[isbn]

    def __len__(self):
        return len(self.books)

    def __repr__(self):
        return f"Library({len(self)} книг)"