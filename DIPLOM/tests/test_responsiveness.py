import allure
import pytest
import time
import requests
from pages.home_page import HomePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Адаптивность сайта")
class TestResponsiveness:
    @allure.story("Проверка адаптивности на мобильных устройствах")
    def test_mobile_responsiveness(self, driver):
        page = HomePage(driver)
        page.open("https://ormea.pl/")

        with allure.step("Установка размера окна для мобильного устройства (375x812)"):
            driver.set_window_size(375, 812)  

        with allure.step("Проверка видимости элементов на мобильном устройстве"):
            assert page.get_logo().is_displayed(), "Логотип не отображается на мобильном устройстве"
            try:
                menu_button = page.get_menu_button()
                assert menu_button.is_displayed(), "Кнопка меню не отображается на мобильном устройстве"
            except Exception as e:
                pytest.fail(f"Элемент меню не найден: {e}")

        with allure.step("Переход на страницу 'Usługi'"):
            try:
                services_link = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.LINK_TEXT, "Usługi"))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", services_link)
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Usługi"))
                )
                driver.execute_script("arguments[0].click();", services_link)
                WebDriverWait(driver, 10).until(EC.url_contains("uslugi"))
                assert "uslugi" in driver.current_url, "Переход на страницу 'Usługi' не произошел"
            except Exception as e:
                pytest.fail(f"Не удалось перейти на страницу 'Usługi': {e}")
        driver.back()

        with allure.step("Открытие контактной формы"):
            try:
                contact_button = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.LINK_TEXT, "Kontakt"))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", contact_button)
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Kontakt"))
                ).click()
                WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "a[href^='tel:']"))
                )
                assert driver.find_element(By.CSS_SELECTOR, "a[href^='tel:']").is_displayed(), "Контактная форма не открылась"
            except Exception as e:
                pytest.fail(f"Не удалось открыть контактную форму: {e}")

    @allure.story("Проверка адаптивности на планшетах")
    def test_tablet_responsiveness(self, driver):
        page = HomePage(driver)
        page.open("https://ormea.pl/")

        with allure.step("Установка размера окна для планшета (768x1024)"):
            driver.set_window_size(768, 1024) 

        with allure.step("Проверка видимости элементов на планшете"):
            assert page.get_logo().is_displayed(), "Логотип не отображается на планшете"
            try:
                nav_menu = page.get_nav_menu()
                assert nav_menu.is_displayed(), "Меню навигации не отображается на планшете"
            except Exception as e:
                pytest.fail(f"Меню навигации не найдено: {e}")

        with allure.step("Переход на русскую версию сайта"):
            try:
                russian_language_link = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//a[@href='https://ormea.pl/ru/']"))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", russian_language_link)
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@href='https://ormea.pl/ru/']"))
                )
                driver.execute_script("arguments[0].click();", russian_language_link)
                WebDriverWait(driver, 10).until(EC.url_contains("ru"))
                assert "ru" in driver.current_url, "Переход на русскую версию сайта не произошел"
            except Exception as e:
                pytest.fail(f"Не удалось перейти на русскую версию сайта: {e}")

@allure.story("Проверка оптимизации изображений")
def test_image_optimization(setup):
    home_page = setup
    max_image_size_kb = 500  

    with allure.step("Открытие главной страницы"):
        home_page.open("https://ormea.pl/")

    with allure.step("Поиск всех изображений на странице"):
        images = home_page.driver.find_elements(By.TAG_NAME, "img")
        assert len(images) > 0, "На странице не найдено изображений"

    with allure.step("Проверка размера каждого изображения"):
        for image in images:
            src = image.get_attribute("src")
            if src:  
                response = requests.get(src, stream=True)
                image_size_kb = int(response.headers.get("content-length", 0)) / 1024

                allure.attach(
                    f"Изображение: {src}\nРазмер: {image_size_kb:.2f} КБ\nДопустимый размер: {max_image_size_kb} КБ",
                    name="Информация о размере изображения",
                    attachment_type=allure.attachment_type.TEXT
                )

                if image_size_kb > max_image_size_kb:
                    allure.attach(
                        f"Изображение {src} имеет размер {image_size_kb:.2f} КБ, что превышает допустимый размер {max_image_size_kb} КБ",
                        name="Превышение размера изображения",
                        attachment_type=allure.attachment_type.TEXT
                    )