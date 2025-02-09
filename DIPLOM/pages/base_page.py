from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

class BasePage:
    BACK_TO_TOP_BUTTON = (By.CSS_SELECTOR, "div.back-to-top")

    def __init__(self, driver):
        self.driver = driver

    def open_url(self, url):
        self.driver.get(url)

    def find_element(self, locator):
        return self.driver.find_element(*locator)

    def wait_for_element(self, locator, timeout=20):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            self.driver.save_screenshot(f"timeout_error_{locator[1]}.png")
            raise TimeoutException(f"Элемент {locator} не найден в течение {timeout} секунд.")

    def click_element(self, locator):
        element = self.wait_for_element(locator)
        element.click()
        
    def is_back_to_top_button_visible(self):
        back_to_top_button = self.wait_for_element(self.BACK_TO_TOP_BUTTON)
        return back_to_top_button.is_displayed()