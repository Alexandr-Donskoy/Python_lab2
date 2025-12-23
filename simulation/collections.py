from .book import Book


class BookCollection:
    def __init__(self, books=None):
        self._books = list(books) if books else []

    def __getitem__(self, key):
        if isinstance(key, slice):
            return BookCollection(self._books[key])
        return self._books[key]

    def __len__(self):
        return len(self._books)

    def __iter__(self):
        return iter(self._books)

    def __contains__(self, item):
        return item in self._books

    def add(self, book):
        self._books.append(book)

    def remove(self, book):
        self._books.remove(book)

    def __repr__(self):
        return f"BookCollection({len(self._books)} books)"


class IndexDict:
    def __init__(self):
        self._isbn_index = {}
        self._author_index = {}
        self._year_index = {}

    def __setitem__(self, key, book):
        if not isinstance(book, Book):
            raise ValueError("Только объекты Book могут быть добавлены в индекс")

        self._isbn_index[book.isbn] = book
        self._author_index.setdefault(book.author, []).append(book)
        self._year_index.setdefault(book.year, []).append(book)

    def __delitem__(self, key):
        book = self._isbn_index.get(key)
        if book:
            del self._isbn_index[key]
            self._author_index[book.author].remove(book)
            self._year_index[book.year].remove(book)

    def __getitem__(self, key):
        return self._isbn_index.get(key)

    def get_by_author(self, author):
        return self._author_index.get(author, [])

    def get_by_year(self, year):
        return self._year_index.get(year, [])

    def __len__(self):
        return len(self._isbn_index)

    def __iter__(self):
        return iter(self._isbn_index.values())

    def __repr__(self):
        return f"IndexDict({len(self._isbn_index)} books)"