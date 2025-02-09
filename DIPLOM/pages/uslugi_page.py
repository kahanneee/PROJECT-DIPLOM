from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class UslugiPage(BasePage):
    
    HEADER = (By.CSS_SELECTOR, "div.heading h1")  
    SERVICE_CARDS = (By.CSS_SELECTOR, ".col-lg-4")  
    FIRST_SERVICE_TITLE = (By.CSS_SELECTOR, ".col-lg-4 .title h3")  
    CONTACT_BUTTON = (By.CSS_SELECTOR, "div.fixed-contact[data-bs-title='Kontakt']")  

    def __init__(self, driver):
        super().__init__(driver)

    def open(self, url="https://ormea.pl/uslugi/"):
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
        
    def get_header_text(self):
        return WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.HEADER)
        ).text
        
    def get_service_cards_count(self):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(self.SERVICE_CARDS)
        )
        return len(self.driver.find_elements(*self.SERVICE_CARDS))

    def get_first_service_title(self):
        return WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.FIRST_SERVICE_TITLE)
        ).text

    def click_contact_button(self):
        return WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.CONTACT_BUTTON)
        ).click()