import random
import sys
from io import StringIO

from simulation.book import Book
from simulation.collections import BookCollection, IndexDict
from simulation.library import Library
from simulation.simulation import run_simulation


# 1. Book Tests
def test_book():
    book = Book("1984", "Оруэлл", 1949, "Фантастика", "ISBN_001")
    assert book.title == "1984"
    assert book.author == "Оруэлл"
    assert repr(book) == "Book('1984', 'Оруэлл', 1949, 'Фантастика', 'ISBN_001')"

    book2 = Book("Скотный двор", "Оруэлл", 1945, "Фантастика", "ISBN_001")
    assert book == book2  # По ISBN

    book3 = Book("1984", "Оруэлл", 1949, "Фантастика", "ISBN_002")
    assert book != book3


# 2. BookCollection Tests
def test_book_collection():
    collection = BookCollection()
    book1 = Book("Книга1", "Автор1", 2000, "Жанр", "ISBN_001")
    book2 = Book("Книга2", "Автор2", 2001, "Жанр", "ISBN_002")

    # Добавление и длина
    collection.add(book1)
    collection.add(book2)
    assert len(collection) == 2

    # Доступ по индексу
    assert collection[0] == book1
    assert collection[1] == book2

    # Срез
    sliced = collection[0:1]
    assert len(sliced) == 1
    assert isinstance(sliced, BookCollection)

    # Итерация
    books = list(collection)
    assert books == [book1, book2]

    # Проверка вхождения
    assert book1 in collection
    assert Book("Нет", "Нет", 0, "Нет", "ISBN_999") not in collection

    # Удаление
    collection.remove(book1)
    assert len(collection) == 1
    assert book1 not in collection


# 3. IndexDict Tests
def test_index_dict():
    index = IndexDict()
    book1 = Book("Книга1", "Автор", 2000, "Жанр", "ISBN_001")
    book2 = Book("Книга2", "Автор", 2001, "Жанр", "ISBN_002")
    book3 = Book("Книга3", "Другой", 2000, "Жанр", "ISBN_003")

    # Добавление
    index[book1.isbn] = book1
    index[book2.isbn] = book2
    index[book3.isbn] = book3

    assert len(index) == 3
    assert index["ISBN_001"] == book1

    # Поиск по автору
    books_by_author = index.get_by_author("Автор")
    assert len(books_by_author) == 2
    assert book1 in books_by_author
    assert book2 in books_by_author

    # Поиск по году
    books_by_year = index.get_by_year(2000)
    assert len(books_by_year) == 2
    assert book1 in books_by_year
    assert book3 in books_by_year

    # Удаление
    del index["ISBN_001"]
    assert len(index) == 2
    assert index["ISBN_001"] is None
    assert len(index.get_by_author("Автор")) == 1
    assert len(index.get_by_year(2000)) == 1

    # Итерация
    books = list(index)
    assert len(books) == 2


# 4. Library Tests
def test_library():
    library = Library()
    book1 = Book("Книга1", "Автор", 2000, "Жанр", "ISBN_001")
    book2 = Book("Книга2", "Автор", 2001, "Жанр", "ISBN_002")

    # Добавление
    library.add_book(book1)
    library.add_book(book2)
    assert len(library) == 2

    # Поиск
    found = library.find_by_author("Автор")
    assert len(found) == 2

    found = library.find_by_year(2000)
    assert len(found) == 1
    assert found[0] == book1

    found = library.find_by_isbn("ISBN_001")
    assert found == book1

    # Удаление
    library.remove_book("ISBN_001")
    assert len(library) == 1
    assert library.find_by_isbn("ISBN_001") is None


# 5. Simulation Tests
def test_simulation_with_seed():
    # Проверяем воспроизводимость с seed
    seed = 123

    output1 = StringIO()
    sys.stdout = output1
    run_simulation(steps=5, seed=seed)
    sys.stdout = sys.__stdout__
    result1 = output1.getvalue()

    output2 = StringIO()
    sys.stdout = output2
    run_simulation(steps=5, seed=seed)
    sys.stdout = sys.__stdout__
    result2 = output2.getvalue()

    assert result1 == result2  # Одинаковый seed = одинаковый вывод


def test_simulation_output():
    # Проверяем, что симуляция выводит шаги
    output = StringIO()
    sys.stdout = output
    run_simulation(steps=2, seed=456)
    sys.stdout = sys.__stdout__
    result = output.getvalue()

    assert "Шаг 1:" in result
    assert "Шаг 2:" in result
    assert "Симуляция завершена" in result


def test_simulation_different_seeds():
    # Разные seed дают разный вывод
    output1 = StringIO()
    sys.stdout = output1
    run_simulation(steps=3, seed=111)
    sys.stdout = sys.__stdout__

    output2 = StringIO()
    sys.stdout = output2
    run_simulation(steps=3, seed=222)
    sys.stdout = sys.__stdout__


# 6. Integration Test
def test_integration():
    # Сквозной тест: создание → коллекция → библиотека → поиск
    library = Library()

    # Добавляем книги
    books = [
        Book("Война и мир", "Толстой", 1869, "Роман", "ISBN_001"),
        Book("Анна Каренина", "Толстой", 1877, "Роман", "ISBN_002"),
        Book("Преступление и наказание", "Достоевский", 1866, "Роман", "ISBN_003"),
    ]

    for book in books:
        library.add_book(book)

    assert len(library) == 3

    # Поиск по автору
    tolsto_books = library.find_by_author("Толстой")
    assert len(tolsto_books) == 2

    # Поиск по году
    books_1869 = library.find_by_year(1869)
    assert len(books_1869) == 1
    assert books_1869[0].title == "Война и мир"

    # Поиск по ISBN
    book = library.find_by_isbn("ISBN_003")
    assert book.title == "Преступление и наказание"

    # Удаление
    library.remove_book("ISBN_001")
    assert len(library) == 2
    assert library.find_by_isbn("ISBN_001") is None


# Запуск всех тестов
if __name__ == "__main__":
    print("Запуск тестов:")

    test_book()
    print(" Book tests passed - пройдено")

    test_book_collection()
    print(" BookCollection tests passed - пройдено")

    test_index_dict()
    print(" IndexDict tests passed - пройдено")

    test_library()
    print(" Library tests passed - пройдено")

    test_simulation_with_seed()
    print(" Simulation seed test passed - пройдено")

    test_simulation_output()
    print(" Simulation output test passed - пройдено")

    test_simulation_different_seeds()
    print(" Simulation different seeds test passed - пройдено")

    test_integration()
    print(" Integration test passed - пройдено")

    print("\n Все тесты пройдены!")