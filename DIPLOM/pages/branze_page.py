from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage

class BranzePage(BasePage):
    # Локаторы элементов
    FOOTER = (By.CSS_SELECTOR, "div.footer-wrapper")
    INDUSTRY_CARD_LINK = (By.CSS_SELECTOR, "div.col-lg-4.col-md-4.col-sm-6.col-6 > a")
    LOGO_CLICK = (By.CSS_SELECTOR, "a.navbar-brand")
    EMAIL_LINK = (By.CSS_SELECTOR, "div.email-data a[href^='mailto:']")
    BACK_TO_TOP_BUTTON = (By.CSS_SELECTOR, "div.back-to-top")
    
    def __init__(self, driver):
        self.driver = driver     
        
    def open(self):
        self.driver.get("https://ormea.pl/branze/")
        self.wait_for_page_to_load()  
    
    def wait_for_page_to_load(self, timeout=20):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            self.driver.save_screenshot("page_load_timeout.png")
            raise TimeoutException(f"Страница не загрузилась в течение {timeout} секунд.")
    
    def is_footer_displayed(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        footer = self.wait_for_element(self.FOOTER)
        return footer.is_displayed()
    
    def is_industry_card_clickable(self):
        element = self.wait_for_element(self.INDUSTRY_CARD_LINK)
        return element.is_displayed() and element.is_enabled()

    def click_logo(self):
        logo = self.wait_for_element(self.LOGO_CLICK)
        logo.click()

    def is_logo_displayed(self):
        logo = self.wait_for_element(self.LOGO_CLICK)
        return logo.is_displayed()

    def is_logo_clickable(self):
        logo = self.wait_for_element(self.LOGO_CLICK)
        return logo.is_enabled()

    def is_email_link_displayed(self):
        email_link = self.wait_for_element(self.EMAIL_LINK)
        return email_link.is_displayed()

    def is_back_to_top_button_visible(self):
        back_to_top_button = self.wait_for_element(self.BACK_TO_TOP_BUTTON)
        return back_to_top_button.is_displayed()