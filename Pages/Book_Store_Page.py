from playwright.sync_api import Page

class BookStorePage:
    def __init__(self, page: Page):
        self.page = page
        self.book_list = page.locator(".rt-tbody .rt-tr-group")

    def open(self):
        self.page.goto("https://demoqa.com/books")

    def get_all_books(self):
        return [book.inner_text() for book in self.book_list.all()]

    def is_book_present(self, book_name):
        return any(book_name in b for b in self.get_all_books())
