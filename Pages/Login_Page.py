from playwright.sync_api import Page, expect
from DemoQA_AutoTest.conftest import BASE_URL

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.page_widgets_menu = page.locator('text=Book Store Application')
        self.page_login = page.locator('li >> text=Login')
        self.user_input = page.locator('#userName')
        self.password_input = page.locator('#password')
        self.login_button = page.locator('#login')

    def open_site(self):
        self.page.goto(BASE_URL)

    def open_login_page(self):
        self.page_widgets_menu.click()
        expect(self.page_login).to_be_visible()
        self.page_login.click()
        expect(self.user_input).to_be_visible()

    def login(self, username, password):
        self.user_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        expect(self.page.get_by_role("button", name="Log out")).to_be_visible()