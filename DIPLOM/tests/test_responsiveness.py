import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.home_page import HomePage  

@allure.feature("Адаптивность сайта")
class TestResponsiveness:

    @allure.story("Адаптивность сайта на мобильных устройствах")
    def test_mobile_responsiveness(self, home_setup):
        page = home_setup

        with allure.step("Установка размера окна для мобильного устройства (375x812)"):
            page.driver.set_window_size(375, 812)  

        self.verify_mobile_elements(page)
        self.verify_navigation_to_services(page)
        self.verify_contact_form(page)

    def verify_mobile_elements(self, page):
        with allure.step("Проверка видимости элементов на мобильном устройстве"):
            assert page.get_logo().is_displayed(), "Логотип не отображается на мобильном устройстве"
            try:
                menu_button = page.get_menu_button()
                assert menu_button.is_displayed(), "Кнопка меню не отображается на мобильном устройстве"
            except Exception as e:
                pytest.fail(f"Элемент меню не найден: {e}")

    def verify_navigation_to_services(self, page):
        with allure.step("Переход на страницу 'Usługi'"):
            try:
                services_link = WebDriverWait(page.driver, 10).until(
                    EC.presence_of_element_located((By.LINK_TEXT, "Usługi"))
                )
                page.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", services_link)
                WebDriverWait(page.driver, 10).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Usługi"))
                )
                page.driver.execute_script("arguments[0].click();", services_link)
                WebDriverWait(page.driver, 10).until(EC.url_contains("uslugi"))
                assert "uslugi" in page.driver.current_url, "Переход на страницу 'Usługi' не произошел"
            except Exception as e:
                pytest.fail(f"Не удалось перейти на страницу 'Usługi': {e}")
        page.driver.back()

    def verify_contact_form(self, page):
        with allure.step("Открытие контактной формы"):
            try:
                contact_button = WebDriverWait(page.driver, 20).until(
                    EC.presence_of_element_located((By.LINK_TEXT, "Kontakt"))
                )
                page.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", contact_button)
                WebDriverWait(page.driver, 20).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Kontakt"))
                ).click()
                WebDriverWait(page.driver, 20).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "a[href^='tel:']"))
                )
                assert page.driver.find_element(By.CSS_SELECTOR, "a[href^='tel:']").is_displayed(), "Контактная форма не открылась"
            except Exception as e:
                pytest.fail(f"Не удалось открыть контактную форму: {e}")

    @allure.story("Адаптивность сайта на планшетах")
    def test_tablet_responsiveness(self, home_setup):
        page = home_setup

        with allure.step("Установка размера окна для планшета (768x1024)"):
            page.driver.set_window_size(768, 1024) 

        self.verify_tablet_elements(page)
        self.verify_language_switch(page)

    def verify_tablet_elements(self, page):
        with allure.step("Проверка видимости элементов на планшете"):
            assert page.get_logo().is_displayed(), "Логотип не отображается на планшете"
            try:
                nav_menu = page.get_nav_menu()
                assert nav_menu.is_displayed(), "Меню навигации не отображается на планшете"
            except Exception as e:
                pytest.fail(f"Меню навигации не найдено: {e}")

    def verify_language_switch(self, page):
        with allure.step("Переход на русскую версию сайта"):
            try:
                russian_language_link = WebDriverWait(page.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//a[@href='https://ormea.pl/ru/']"))
                )
                page.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", russian_language_link)
                WebDriverWait(page.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@href='https://ormea.pl/ru/']"))
                )
                page.driver.execute_script("arguments[0].click();", russian_language_link)
                WebDriverWait(page.driver, 10).until(EC.url_contains("ru"))
                assert "ru" in page.driver.current_url, "Переход на русскую версию сайта не произошел"
            except Exception as e:
                pytest.fail(f"Не удалось перейти на русскую версию сайта: {e}")
