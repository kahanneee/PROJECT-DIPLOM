import allure
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from axe_selenium_python import Axe
from PIL import ImageColor

@allure.feature("Доступность сайта")
def test_accessibility(driver):
    with allure.step("Открываем сайт https://ormea.pl/"):
        driver.get("https://ormea.pl/")

    with allure.step("Инициализируем Axe и запускаем анализ доступности"):
        axe = Axe(driver)
        axe.inject()
        results = axe.run()
        axe.write_results(results, "accessibility_results.json")

    with allure.step("Фильтрация игнорируемых нарушений"):
        ignored_violations = ["aria-allowed-role", "color-contrast"]
        filtered_violations = [violation for violation in results["violations"] if violation["id"] not in ignored_violations]

    with allure.step("Проверка наличия нарушений доступности"):
        assert len(filtered_violations) == 0, f"Обнаружены нарушения доступности: {filtered_violations}"

@allure.feature("Контрастность текста")
def test_contrast(driver):
    def get_luminance(rgb):
        r, g, b = [x / 255.0 for x in rgb[:3]]
        r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
        g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
        b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    def calculate_contrast_ratio(color1, color2):
        luminance1 = get_luminance(color1)
        luminance2 = get_luminance(color2)
        return (luminance1 + 0.05) / (luminance2 + 0.05) if luminance1 > luminance2 else (luminance2 + 0.05) / (luminance1 + 0.05)

    with allure.step("Открываем сайт https://ormea.pl/"):
        driver.get("https://ormea.pl/")

    with allure.step("Проверяем контрастность для body элемента"):
        element = driver.find_element(By.CSS_SELECTOR, "body")
        color = element.value_of_css_property("color")
        background_color = element.value_of_css_property("background-color")

        text_rgb = ImageColor.getrgb(color)
        background_rgb = ImageColor.getrgb(background_color)

        contrast_ratio = calculate_contrast_ratio(text_rgb, background_rgb)
        assert contrast_ratio >= 4.5, f"Контрастность ({contrast_ratio:.2f}) ниже минимального требования WCAG 4.5."
        allure.attach(f"Цвет текста: {color}\nЦвет фона: {background_color}\nКонтрастность: {contrast_ratio:.2f}", name="Результаты проверки контрастности")
