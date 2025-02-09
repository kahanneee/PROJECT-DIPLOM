from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class HomePage(BasePage):
    LOGO = (By.CSS_SELECTOR, "a.navbar-brand img")
    CONTACT_PHONE = (By.CSS_SELECTOR, "a[href^='tel:']")
    CONTACT_EMAIL = (By.CSS_SELECTOR, "a[href^='mailto:']")
    FORM = (By.CSS_SELECTOR, "form")
    NAV_MENU = (By.CSS_SELECTOR, "nav a")
    NAV_MENU_ITEMS = (By.CSS_SELECTOR, "nav a")
    MENU_BOTTON = (By.CSS_SELECTOR, "button[aria-label='Toggle navigation']")
    LINKEDIN_LINK = (By.CSS_SELECTOR, "a.nav-link[href*='linkedin.com']")
    CLOSE_BUTTON = (By.CSS_SELECTOR, "svg.artdeco-icon[aria-busy='false']")
    LOGO_CLICK = (By.CSS_SELECTOR, "a.navbar-brand")
        
    def __init__(self, driver):
        self.driver = driver

    def open(self, url):        
        self.driver.get(url)

    def get_logo(self):
        return self.wait_for_element(self.LOGO)

    def get_contact_phone_locator(self):
        return self.CONTACT_PHONE

    def get_contact_email_locator(self):
        return self.CONTACT_EMAIL

    def get_service_form(self):
        return self.wait_for_element(self.FORM)

    def get_nav_menu(self):
        return self.driver.find_element(*self.NAV_MENU)
    
    def get_nav_menu_items(self):
        return self.driver.find_elements(*self.NAV_MENU_ITEMS)
    
    def get_menu_button(self):
        return self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Toggle navigation']")
    
    def click_linkedin_link(self):
        linkedin_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.LINKEDIN_LINK)
        )
        linkedin_link.click()

    def is_linkedin_page_opened(self):
        WebDriverWait(self.driver, 20).until(lambda d: "linkedin.com" in d.current_url)
        return "linkedin.com" in self.driver.current_url
       
        WebDriverWait(self.driver, 20).until(lambda d: "linkedin.com" in d.current_url)
        return "linkedin.com" in self.driver.current_url
    
    def close_modal(self):
        try:
            close_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.CLOSE_BUTTON)
            )
            close_button.click()
        except Exception as e:
            print(f"Не удалось закрыть модальное окно: {e}")    
            
    def click_logo(self):
        logo = self.wait_for_element(self.LOGO_CLICK)
        logo.click()

    def is_logo_displayed(self):
        logo = self.wait_for_element(self.LOGO_CLICK)
        return logo.is_displayed()
