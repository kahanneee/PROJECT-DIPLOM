import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage

@allure.feature("Главная страница")
@allure.story("Проверка загрузки страницы")
def test_home_page_loads_successfully(setup):
    with allure.step("Проверка заголовка страницы"):
        assert "Ormea" in setup.driver.title, "Заголовок страницы не содержит 'Ormea'"

@allure.story("Проверка меню навигации")
def test_navigation_menu(setup):
    with allure.step("Получение элементов меню"):
        menu_items = setup.get_nav_menu_items()
    with allure.step("Проверка, что меню содержит ссылки"):
        assert len(menu_items) > 0, "Меню не содержит ссылок"

@allure.story("Проверка контактной информации")
def test_contact_page_has_phone_and_email(setup):
    with allure.step("Получение элемента телефона"):
        phone = setup.get_contact_phone()
    with allure.step("Получение элемента email"):
        email = setup.get_contact_email()
    with allure.step("Проверка отображения телефона и email"):
        assert phone.is_displayed(), "Телефон не найден"
        assert email.is_displayed(), "Email не найден"

@allure.story("Проверка формы запроса услуг")
def test_service_request_form_is_accessible(setup):
    with allure.step("Получение элемента формы"):
        form = setup.get_service_form()
    with allure.step("Проверка отображения формы"):
        assert form.is_displayed(), "Форма запроса услуг не доступна"

@allure.story("Проверка отображения логотипа")
def test_logo_is_displayed(setup):
    """Проверка, что логотип отображается на странице."""
    with allure.step("Получение элемента логотипа"):
        logo = setup.get_logo()
    with allure.step("Проверка отображения логотипа"):
        assert logo.is_displayed(), "Логотип не отображается"
 
@allure.story("Проверка смены языка")
def test_language_switch(setup):
    base_url = "https://ormea.pl/"  

    with allure.step("Проверка смены языка на английский"):
        try:
            english_link = WebDriverWait(setup.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[@href='https://ormea.pl/en/']"))
            )
            english_link.click()
            
            WebDriverWait(setup.driver, 10).until(EC.url_to_be("https://ormea.pl/en/"))
            assert setup.driver.current_url == "https://ormea.pl/en/", "Переключение на английский язык не произошло"
        except Exception as e:
            pytest.fail(f"Ошибка при переключении на английский язык: {e}")

    with allure.step("Проверка смены языка на русский"):
        try:
            setup.driver.get(base_url)  

            russian_link = WebDriverWait(setup.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[@href='https://ormea.pl/ru/']"))
            )
            russian_link.click()

            WebDriverWait(setup.driver, 10).until(EC.url_to_be("https://ormea.pl/ru/"))
            assert setup.driver.current_url == "https://ormea.pl/ru/", "Переключение на русский язык не произошло"
        except Exception as e:
            pytest.fail(f"Ошибка при переключении на русский язык: {e}")

@allure.story("Проверка перехода на социальные сети")
def test_linkedin_link_redirects_correctly(setup):
    home_page = setup
    home_page.open("https://ormea.pl/")

    with allure.step("Клик на ссылку LinkedIn"):
        home_page.click_linkedin_link()
        
    with allure.step("Закрытие всплывающего окна"):
        home_page.close_modal()
        
    with allure.step("Проверка, что открылась страница LinkedIn"):
        assert home_page.is_linkedin_page_opened(), "Переход на LinkedIn не произошел"
            
    with allure.step("Закрытие вкладки LinkedIn и возврат на главную страницу"):
        if len(home_page.driver.window_handles) > 1:
            home_page.driver.close() 
            home_page.driver.switch_to.window(home_page.driver.window_handles[0])  # Переключаемся на главную вкладку