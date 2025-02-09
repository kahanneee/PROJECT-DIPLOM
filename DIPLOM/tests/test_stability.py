import pytest
import allure
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urljoin

@allure.feature("Нагрузочное тестирование")
@allure.story("Перегрузка сервера")
def test_server_overload(driver):
    url = "https://ormea.pl"
    num_requests = 100
    failed_requests = 0

    for _ in range(num_requests):
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except Exception:
            failed_requests += 1
    assert failed_requests == 0, f"Количество неудачных запросов: {failed_requests}"

@allure.feature("Обработка ошибок")
@allure.story("Страница 404")
def test_404_page(driver):
    base_url = "https://ormea.pl/"
    non_existent_url = urljoin(base_url, "non-existent-page")

    with allure.step("Переход на несуществующую страницу"):
        driver.get(non_existent_url)

    with allure.step("Проверка наличия 404 ошибки"):
        try:
            response = requests.get(non_existent_url, allow_redirects=True, timeout=10)
            assert response.status_code == 404, f"Ожидался статус 404, получен {response.status_code}"
        except requests.RequestException as e:
            pytest.fail(f"Ошибка при проверке 404 страницы: {e}")

@allure.feature("Обработка ошибок")
@allure.story("Отсутствие ошибки 500")
def test_no_500_error(driver):
    base_url = "https://ormea.pl/"
    test_url = urljoin(base_url, "some-page")

    with allure.step("Переход на тестовую страницу"):
        driver.get(test_url)

    with allure.step("Проверка отсутствия ошибки 500"):
        try:
            response = requests.get(test_url, allow_redirects=True, timeout=10)
            assert response.status_code != 500, f"Получен статус 500 на странице {test_url}"
        except requests.RequestException as e:
            pytest.fail(f"Ошибка при проверке страницы: {e}")

@allure.feature("Тестирование без интернета")
@allure.story("Работа без подключения к интернету")
def test_no_internet_connection(driver):
    url = "https://ormea.pl"

    with allure.step("Отключение интернета"):
        import os
        os.system("ipconfig /release")

    with allure.step("Попытка работы с сайтом без интернета"):
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            pytest.fail("Страница загрузилась без интернет-соединения")
        except Exception as e:
            allure.attach(str(e), name="Ошибка без интернета", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Включение интернета"):
        os.system("ipconfig /renew")

@allure.feature("Недоступные ресурсы")
@allure.story("Проверка недоступных изображений")
def test_unavailable_resources(driver):
    url = "https://ormea.pl"
    driver.get(url)

    with allure.step("Имитируем недоступные ресурсы"):
        try:
            images = driver.find_elements(By.TAG_NAME, "img")
            broken_images = []
            for img in images:
                src = img.get_attribute("src")
                response = requests.head(src, allow_redirects=True, timeout=10)
                if response.status_code >= 400:
                    broken_images.append((src, response.status_code))

            assert not broken_images, f"Найдены недоступные изображения: {broken_images}"
        except Exception as e:
            pytest.fail(f"Ошибка при проверке недоступных ресурсов: {e}")

@allure.feature("Медленное интернет-соединение")
@allure.story("Работа при медленном соединении")
def test_slow_internet_connection(driver_stability):
    url = "https://ormea.pl"

    with allure.step("Установка низкой скорости соединения"):
        driver_stability.execute_cdp_cmd(
            "Network.enable", {}
        )
        driver_stability.execute_cdp_cmd(
            "Network.emulateNetworkConditions", {
                "offline": False,
                "latency": 200, 
                "downloadThroughput": 500 * 1024 / 8,  
                "uploadThroughput": 500 * 1024 / 8  
            }
        )

    with allure.step("Попытка работы с сайтом на медленном соединении"):
        driver_stability.get(url)
        try:
            WebDriverWait(driver_stability, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        except Exception as e:
            pytest.fail(f"Ошибка при медленном соединении: {e}")