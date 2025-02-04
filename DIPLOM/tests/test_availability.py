from selenium import webdriver
from axe_selenium_python import Axe
import pytest
from selenium.webdriver.common.by import By
import allure

# Функция для проверки доступности с помощью axe-core
@allure.feature("Accessibility Testing")
def test_accessibility():
    driver = webdriver.Chrome()

    try:
        with allure.step("Открываем сайт https://ormea.pl/"):
            driver.get("https://ormea.pl/")

        with allure.step("Инициализируем Axe и запускаем проверку доступности"):
            axe = Axe(driver)
            axe.inject()
            results = axe.run()
            axe.write_results(results, "accessibility_results.json")

        with allure.step("Игнорируем определенные нарушения"):
            ignored_violations = [
                "aria-allowed-role",  
                "color-contrast",     
            ]

            filtered_violations = [
                violation for violation in results["violations"]
                if violation["id"] not in ignored_violations
            ]

        with allure.step("Проверяем, есть ли нарушения"):
            assert len(filtered_violations) > 0, f"Нарушения доступности не найдены, но они должны быть: {filtered_violations}"

    finally:
        with allure.step("Закрываем браузер"):
            driver.quit()

# Функция для проверки контрастности 
@allure.feature("Contrast Testing")
def test_contrast():
    driver = webdriver.Chrome()

    try:
        with allure.step("Открываем сайт https://ormea.pl/"):
            driver.get("https://ormea.pl/")

        with allure.step("Проверяем контрастность для конкретного элемента"):
            element = driver.find_element(By.CSS_SELECTOR, "body") 
            color = element.value_of_css_property("color")  
            background_color = element.value_of_css_property("background-color")  
           
    finally:
        with allure.step("Закрываем браузер"):
            driver.quit()

