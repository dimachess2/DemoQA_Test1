def compare_books(api_books: list[str], ui_books: list[str]):
    ui_book_titles = [
        b.split("\n")[0].strip()
        for b in ui_books
        if b.strip() and not all(c in '\xa0 ' for c in b.split("\n")[0].strip())
    ]
    print(f"[UI]  Книги: {ui_book_titles}")

    for book in api_books:
        assert book in ui_book_titles, f"[ERROR] Книга из API не найдена на UI: {book}"

    for book in ui_book_titles:
        assert book in api_books, f"[ERROR] Книга на UI отсутствует в API: {book}"

    print("[CHECK] UI и API книги совпадают ✅")