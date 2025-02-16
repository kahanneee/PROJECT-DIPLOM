import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.uslugi_page import UslugiPage  

@allure.feature("Страница услуг")
class TestUslugiPage:

    @allure.story("Отображение заголовка страницы")
    def test_header_text(self, uslugi_setup):
        page = uslugi_setup
        with allure.step("Проверка заголовка страницы"):
            header_text = page.get_header_text()
            assert header_text == "USŁUGI", f"Заголовок страницы '{header_text}' не соответствует ожидаемому"

    @allure.story("Количество карточек услуг")
    def test_service_cards_count(self, uslugi_setup):
        page = uslugi_setup
        with allure.step("Проверка количества карточек услуг"):
            cards_count = page.get_service_cards_count()
            assert cards_count > 0, "Карточки услуг отсутствуют"

    @allure.story("Заголовок первой услуги")
    def test_first_service_title(self, uslugi_setup):
        page = uslugi_setup
        with allure.step("Проверка заголовка первой услуги"):
            first_service_title = page.get_first_service_title()
            assert first_service_title == "POMOC Z WYKUPEM I OBSŁUGĄ TOWARU", f"Заголовок первой услуги '{first_service_title}' не соответствует ожидаемому"

    @allure.story("Функциональность кнопки 'Связаться'")
    def test_contact_button(self, uslugi_setup):
        page = uslugi_setup
        with allure.step("Клик по кнопке 'Связаться'"):
            page.click_contact_button()
            assert "kontakt" in page.driver.current_url, "Кнопка 'Связаться' не ведет на правильную страницу"

    @allure.story("Отображение всех элементов на странице")
    def test_page_elements_visibility(self, uslugi_setup):
        page = uslugi_setup
        with allure.step("Проверка видимости заголовка страницы"):
            assert page.wait_for_element(page.HEADER), "Заголовок страницы не отображается"
        with allure.step("Проверка видимости карточек услуг"):
            assert page.wait_for_element(page.SERVICE_CARDS), "Карточки услуг отсутствуют"
        with allure.step("Проверка видимости заголовка первой услуги"):
            assert page.wait_for_element(page.FIRST_SERVICE_TITLE), "Заголовок первой услуги не отображается"
        with allure.step("Проверка видимости кнопки 'Связаться'"):
            assert page.wait_for_element(page.CONTACT_BUTTON), "Кнопка 'Связаться' не отображается"
