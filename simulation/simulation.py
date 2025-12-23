import random
from .book import Book
from .library import Library

def run_simulation(steps=20, seed=None):
    if seed is not None:
        random.seed(seed)

    library = Library()
    genres = ["Фантастика", "Детектив", "Роман", "Научная литература", "Поэзия"]
    authors = ["Толстой", "Достоевский", "Оруэлл", "Брэдбери", "Кинг"]

    for step in range(1, steps + 1):
        print(f"\nШаг {step}:")
        event = random.choice([
            "add_book",
            "remove_random_book",
            "search_by_author",
            "search_by_year",
            "update_index",
            "try_nonexistent"
        ])

        if event == "add_book":
            book = Book(
                title=f"Книга_{step}",
                author=random.choice(authors),
                year=random.randint(1900, 2023),
                genre=random.choice(genres),
                isbn=f"ISBN_{step}"
            )
            library.add_book(book)

        elif event == "remove_random_book" and len(library) > 0:
            book_to_remove = random.choice(list(library.books))
            library.remove_book(book_to_remove.isbn)

        elif event == "search_by_author":
            author = random.choice(authors)
            books = library.find_by_author(author)
            print(f"Поиск по автору '{author}': найдено {len(books)} книг")

        elif event == "search_by_year":
            year = random.randint(1900, 2023)
            books = library.find_by_year(year)
            print(f"Поиск по году {year}: найдено {len(books)} книг")

        elif event == "update_index":
            print("Индекс обновлен")

        elif event == "try_nonexistent":
            fake_isbn = "FAKE_ISBN"
            book = library.find_by_isbn(fake_isbn)
            print(f"Поиск несуществующей книги по ISBN '{fake_isbn}': {book}")

    print(f"\nСимуляция завершена. Всего книг в библиотеке: {len(library)}")