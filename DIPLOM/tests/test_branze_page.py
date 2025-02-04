import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.branze_page import BranzePage
import time
from selenium.common.exceptions import TimeoutException

@pytest.fixture
def setup(driver):
    branze_page = BranzePage(driver)
    branze_page.open()
    yield branze_page
    
@allure.feature("Футер")
def test_footer_is_displayed(setup):
    branze_page = setup
    with allure.step("Проверка видимости футера"):
        assert branze_page.is_footer_displayed(), "Футер не отображается"

@allure.feature("Карточка отрасли")
def test_industry_card_is_clickable(setup):
    branze_page = setup
    with allure.step("Проверка кликабельности карточки отрасли"):
        assert branze_page.is_industry_card_clickable(), "Карточка отрасли не кликабельна"

@allure.feature("Логотип")
def test_logo_redirects_to_home_page(setup):
    branze_page = setup

    with allure.step("Клик по логотипу"):
        branze_page.click_logo()
    
    with allure.step("Ожидание перенаправления на главную страницу"):
        WebDriverWait(branze_page.driver, 20).until(
            EC.url_to_be("https://ormea.pl/")
        )
        assert branze_page.driver.current_url == "https://ormea.pl/", "Перенаправление на главную страницу не произошло"

@allure.feature("Email-ссылка")
def test_email_link_is_displayed(setup):
    branze_page = setup
    with allure.step("Проверка видимости email-ссылки"):
        assert branze_page.is_email_link_displayed(), "Email-ссылка не отображается"

@allure.feature("скрыт ли элемент через CSS")
def is_element_hidden(driver, locator):
    element = driver.find_element(*locator)
    style = element.value_of_css_property("visibility")
    opacity = element.value_of_css_property("opacity")
    return style == "hidden" or opacity == "0"

@allure.feature("Кнопка 'Вверх'")
def test_back_to_top_button_visibility(setup):
    branze_page = setup

    with allure.step("Пролистывание страницы вниз"):
        branze_page.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  

    with allure.step("Ожидание появления кнопки 'Вверх'"):
        try:
            WebDriverWait(branze_page.driver, 10).until(
                EC.visibility_of_element_located(branze_page.BACK_TO_TOP_BUTTON)
            )
            assert branze_page.is_back_to_top_button_visible(), "Кнопка 'Вверх' не появилась после пролистывания"
        except TimeoutException:
            raise AssertionError("Кнопка 'Вверх' не появилась после прокрутки вниз")

    with allure.step("Клик по кнопке 'Вверх'"):
        branze_page.click_element(branze_page.BACK_TO_TOP_BUTTON)

    with allure.step("Ожидание прокрутки страницы вверх"):
        try:
            WebDriverWait(branze_page.driver, 10).until(
                lambda driver: driver.execute_script("return window.pageYOffset == 0;")
            )
        except TimeoutException:
            raise AssertionError("Страница не прокрутилась вверх после нажатия на кнопку 'Вверх'")

    with allure.step("Ожидание скрытия кнопки 'Вверх'"):
        try:
            WebDriverWait(branze_page.driver, 10).until(
                lambda driver: is_element_hidden(driver, branze_page.BACK_TO_TOP_BUTTON)
            )
        except TimeoutException:
            raise AssertionError("Кнопка 'Вверх' не стала скрытой после прокрутки вверх")

    with allure.step("Дополнительная проверка скрытия кнопки"):
        assert is_element_hidden(branze_page.driver, branze_page.BACK_TO_TOP_BUTTON), "Кнопка 'Вверх' все еще видима после прокрутки вверх"