from selenium.webdriver.common.by import By
from .base_page import BasePage

class HomePage(BasePage):
    LOGO = (By.CSS_SELECTOR, "a.navbar-brand img")
    CONTACT_PHONE = (By.CSS_SELECTOR, "a[href^='tel:']")
    CONTACT_EMAIL = (By.CSS_SELECTOR, "a[href^='mailto:']")
    FORM = (By.CSS_SELECTOR, "form")
    NAV_MENU = (By.CSS_SELECTOR, "nav a")
    NAV_MENU_ITEMS = (By.CSS_SELECTOR, "nav a")
    MENU_BOTTON = (By.CSS_SELECTOR, "button[aria-label='Toggle navigation']")

    def __init__(self, driver):
        super().__init__(driver)

    def open(self, url):        
        self.driver.get(url)

    def get_logo(self):
        return self.wait_for_element(self.LOGO)

    def get_contact_phone(self):
        return self.wait_for_element(self.CONTACT_PHONE)

    def get_contact_email(self):
        return self.wait_for_element(self.CONTACT_EMAIL)

    def get_service_form(self):
        return self.wait_for_element(self.FORM)

    def get_nav_menu(self):
        return self.driver.find_element(*self.NAV_MENU)
    
    def get_nav_menu_items(self):
        return self.driver.find_elements(*self.NAV_MENU_ITEMS)
    
    def get_menu_button(self):
        return self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Toggle navigation']")