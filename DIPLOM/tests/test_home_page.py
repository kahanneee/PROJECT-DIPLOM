import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage

@allure.feature("Главная страница")
@allure.story("Загрузка страницы")
def test_home_page_loads_successfully(home_setup):
    with allure.step("Проверка заголовка страницы"):
        assert "Ormea" in home_setup.driver.title, "Заголовок страницы не содержит 'Ormea'"

@allure.story("Меню навигации")
def test_navigation_menu(home_setup):
    with allure.step("Получение элементов меню"):
        menu_items = home_setup.get_nav_menu_items()
    with allure.step("Проверка наличия ссылок в меню"):
        assert len(menu_items) > 0, "Меню не содержит ссылок"

@allure.story("Наличие контактной информации")
def test_contact_page_has_phone_and_email(home_setup):
    with allure.step("Получение элемента телефона"):
        phone_locator = home_setup.get_contact_phone_locator()
    with allure.step("Получение элемента email"):
        email_locator = home_setup.get_contact_email_locator()
    with allure.step("Проверка отображения телефона и email"):
        phone = WebDriverWait(home_setup.driver, 10).until(EC.visibility_of_element_located(phone_locator))
        email = WebDriverWait(home_setup.driver, 10).until(EC.visibility_of_element_located(email_locator))
        assert phone.is_displayed(), "Телефон не найден"
        assert email.is_displayed(), "Email не найден"

@allure.story("Доступность формы запроса услуг")
def test_service_request_form_is_accessible(home_setup):
    with allure.step("Получение элемента формы"):
        form = home_setup.get_service_form()
    with allure.step("Проверка отображения формы"):
        assert form.is_displayed(), "Форма запроса услуг не доступна"

@allure.story("Отображение логотипа")
def test_logo_is_displayed(home_setup):
    with allure.step("Получение элемента логотипа"):
        logo = home_setup.get_logo()
    with allure.step("Проверка отображения логотипа"):
        assert logo.is_displayed(), "Логотип не отображается"

@allure.story("Функциональность смены языка на сайте")
def test_language_switch(home_setup):
    base_url = "https://ormea.pl/"
    languages = {
        "en": "https://ormea.pl/en/",
        "ru": "https://ormea.pl/ru/"
    }
    
    for lang, url in languages.items():
        with allure.step(f"Проверка смены языка на {lang}"):
            try:
                home_setup.driver.get(base_url)
                language_link = WebDriverWait(home_setup.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"//a[@href='{url}']"))
                )
                language_link.click()
                WebDriverWait(home_setup.driver, 10).until(EC.url_to_be(url))
                assert home_setup.driver.current_url == url, f"Переключение на язык {lang} не произошло"
            except Exception as e:
                pytest.fail(f"Ошибка при переключении на язык {lang}: {e}")

@allure.story("Функциональность перехода на социальные сети")
def test_linkedin_link_redirects_correctly(home_setup):
    home_page = home_setup
    with allure.step("Нажатие на ссылку LinkedIn"):
        home_page.click_linkedin_link()
    with allure.step("Закрытие всплывающего окна"):
        home_page.close_modal()
    with allure.step("Проверка, что открылась страница LinkedIn"):
        assert home_page.is_linkedin_page_opened(), "Переход на LinkedIn не произошел"
    with allure.step("Закрытие вкладки LinkedIn и возврат на главную страницу"):
        if len(home_page.driver.window_handles) > 1:
            home_page.driver.close()
            home_page.driver.switch_to.window(home_page.driver.window_handles[0])
