import pytest
import requests
from playwright.sync_api import Page
from DemoQA_AutoTest.Pages.Login_Page import LoginPage
from DemoQA_AutoTest.Pages.Book_Store_Page import BookStorePage
from DemoQA_AutoTest.conftest import BASE_URL
from DemoQA_AutoTest.utils import compare_books
from DemoQA_AutoTest.conftest import test_user


def test_login_valid_user(page: Page, test_user):
    login_page = LoginPage(page)
    login_page.open_site()
    login_page.open_login_page()
    login_page.login(test_user["username"], test_user["password"])
    assert page.url.endswith("/profile")

    response = requests.get(f"{BASE_URL}/BookStore/v1/Books")
    api_books = [b["title"] for b in response.json()["books"]]

    book_page = BookStorePage(page)
    book_page.open()
    ui_books = book_page.get_all_books()

    print(f"[API] Книги: {api_books}")

    compare_books(api_books, ui_books)
