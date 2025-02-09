from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage

class BranzePage(BasePage):
    FOOTER = (By.CSS_SELECTOR, "div.footer-wrapper")
    INDUSTRY_CARD_LINK = (By.CSS_SELECTOR, "div.col-lg-4.col-md-4.col-sm-6.col-6 > a")
    EMAIL_LINK = (By.CSS_SELECTOR, "div.email-data a[href^='mailto:']")
    SOCIAL_LINK = (By.CSS_SELECTOR, "a.nav-link[href*='linkedin.com']")
    
    def __init__(self, driver):
        self.driver = driver     
        
    def open(self, url="https://ormea.pl/branze/"):
        self.driver.get(url)
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
    
    def get_footer_social_links(self):
        return self.driver.find_elements(*self.SOCIAL_LINK)

    def get_footer_contact_info(self):
        return self.wait_for_element(self.EMAIL_LINK)

    def wait_for_element(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
    
    def is_industry_card_clickable(self):
        element = self.wait_for_element(self.INDUSTRY_CARD_LINK)
        return element.is_displayed() and element.is_enabled()

    def is_email_link_displayed(self):
        email_link = self.wait_for_element(self.EMAIL_LINK)
        return email_link.is_displayed()

