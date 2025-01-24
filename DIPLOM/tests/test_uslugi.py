import allure
import pytest
from pages.uslugi_page import UslugiPage

@allure.feature("Страница услуг")
class TestUslugiPage:
    @allure.story("Проверка заголовка страницы")
    def test_header_text(self, driver):  # Используем фикстуру driver
        page = UslugiPage(driver)  # Создаем экземпляр страницы
        driver.get("https://ormea.pl/uslugi/")  # Переходим на страницу
        assert page.get_header_text() == "USŁUGI", "Заголовок страницы не соответствует ожидаемому"

    @allure.story("Проверка количества карточек услуг")
    def test_service_cards_count(self, driver):  # Используем фикстуру driver
        page = UslugiPage(driver)
        driver.get("https://ormea.pl/uslugi/")
        assert page.get_service_cards_count() > 0, "Карточки услуг отсутствуют"

    @allure.story("Проверка заголовка первой услуги")
    def test_first_service_title(self, driver):  # Используем фикстуру driver
        page = UslugiPage(driver)
        driver.get("https://ormea.pl/uslugi/")
        assert page.get_first_service_title() == "POMOC Z WYKUPEM I OBSŁUGĄ TOWARU", "Заголовок первой услуги не соответствует ожидаемому"

    @allure.story("Проверка кнопки 'Связаться'")
    def test_contact_button(self, driver):  # Используем фикстуру driver
        page = UslugiPage(driver)
        driver.get("https://ormea.pl/uslugi/")
        page.click_contact_button()
        assert "kontakt" in driver.current_url, "Кнопка 'Связаться' не ведет на правильную страницу"

    @allure.story("Проверка отображения всех элементов на странице")
    def test_page_elements_visibility(self, driver):  # Используем фикстуру driver
        page = UslugiPage(driver)
        driver.get("https://ormea.pl/uslugi/")
        assert page.wait_for_element(page.HEADER), "Заголовок страницы не отображается"
        assert page.wait_for_element(page.SERVICE_CARDS), "Карточки услуг отсутсвуют"
        assert page.wait_for_element(page.FIRST_SERVICE_TITLE), "Заголовок первой услуги не отображается"
        assert page.wait_for_element(page.CONTACT_BUTTON), "Кнопка 'Связаться' не отображается"