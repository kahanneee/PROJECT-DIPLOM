import allure
import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.story("Проверка скорости загрузки страницы")
def test_page_load_time(setup):
    home_page = setup
    max_load_time = 2  

    with allure.step("Открытие главной страницы"):
        start_time = time.time()
        home_page.open("https://ormea.pl/")
        end_time = time.time()

    load_time = end_time - start_time

    with allure.step(f"Проверка, что страница загрузилась за {max_load_time} секунд"):
        assert load_time <= max_load_time, f"Страница загрузилась за {load_time} секунд, что превышает допустимое время {max_load_time} секунд"          

@allure.feature("Замер времени отклика")
def test_response_time():
    driver = webdriver.Chrome()
   
    try:
        start_time = time.time()
        with allure.step("Загрузка главной страницы"):
            driver.get("https://ormea.pl/")
        
        with allure.step("Ожидание загрузки элемента"):
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        end_time = time.time()
        response_time = end_time - start_time

        with allure.step(f"Время отклика: {response_time} секунд"):
            assert response_time < 3, f"Время отклика слишком велико: {response_time} секунд"

    finally:
        driver.quit()

@allure.feature("Нагрузочное тестирование")
def test_load_testing():
    result = os.system("locust -f locustfile.py --headless -u 100 -r 10 -t 1m")
    assert result == 0, "Нагрузочное тестирование завершилось с ошибкой"
    
@allure.feature("Стресс-тестирование")
def test_stress_testing():
    result = os.system("locust -f locustfile.py --headless -u 1000 -r 100 -t 10m")
    assert result == 0, "Стресс-тестирование завершилось с ошибкой"