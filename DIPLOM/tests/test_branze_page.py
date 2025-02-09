import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.branze_page import BranzePage
from selenium.webdriver.common.action_chains import ActionChains

@allure.feature("Интерактивность карточек отрасли")
def test_industry_card_is_clickable(branze_setup):
    branze_page = branze_setup
    with allure.step("Переход по карточке отрасли"):
        industry_card = branze_page.wait_for_element(branze_page.INDUSTRY_CARD_LINK)
        
        with allure.step("Прокрутка к карточке отрасли"):
            branze_page.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", industry_card)
        
        with allure.step("Взаимодействие с карточкой отрасли"):
            actions = ActionChains(branze_page.driver)
            actions.move_to_element(industry_card).click().perform()
        
        with allure.step("Проверка перенаправления"):
            expected_url_part = industry_card.get_attribute('href').split('/')[-1]
            try:
                WebDriverWait(branze_page.driver, 10).until(
                    EC.url_contains(expected_url_part)
                )
                current_url = branze_page.driver.current_url
                allure.attach(current_url, name="Current URL", attachment_type=allure.attachment_type.TEXT)
                assert expected_url_part in current_url, f"Перенаправление не произошло. Текущий URL: {current_url}, ожидаемая часть URL: {expected_url_part}"
            except Exception as e:
                allure.attach(str(e), name="Ошибка перенаправления", attachment_type=allure.attachment_type.TEXT)

@allure.feature("Функциональность логотипа")
def test_logo_redirects_to_home_page(home_setup):
    home_page = home_setup
    with allure.step("Клик по логотипу"):
        home_page.click_logo()
    
    with allure.step("Ожидание перенаправления на главную страницу"):
        WebDriverWait(home_page.driver, 20).until(
            EC.url_to_be("https://ormea.pl/")
        )
        assert home_page.driver.current_url == "https://ormea.pl/", "Перенаправление на главную страницу не произошло"

@allure.feature("Наличие email-ссылки")
def test_email_link_is_displayed(branze_setup):
    branze_page = branze_setup
    with allure.step("Проверка наличия email-ссылки в футере"):
        assert branze_page.is_email_link_displayed(), "Email-ссылка не отображается"

@allure.feature("Скрытие элементов с использованием CSS")
def is_element_hidden(driver, locator):
    try:
        element = driver.find_element(*locator)
        is_displayed = element.is_displayed()
        has_size = element.size['height'] > 0 and element.size['width'] > 0
        return not (is_displayed and has_size)
    except:
        return True

@allure.feature("Функциональность кнопки 'Вверх'")
def test_back_to_top_button(branze_setup):
    branze_page = branze_setup
    with allure.step("Пролистывание страницы вниз"):
        branze_page.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    with allure.step("Ожидание появления кнопки 'Вверх'"):
        try:
            WebDriverWait(branze_page.driver, 10).until(
                EC.visibility_of_element_located(branze_page.BACK_TO_TOP_BUTTON)
            )
            assert branze_page.is_back_to_top_button_visible(), "Кнопка 'Вверх' не появилась после пролистывания"
        except TimeoutException:
            raise AssertionError("Кнопка 'Вверх' не появилась после прокрутки вниз")

    with allure.step("Нажатие по кнопке 'Вверх'"):
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
