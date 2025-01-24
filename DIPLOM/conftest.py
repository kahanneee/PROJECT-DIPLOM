import pytest
from selenium import webdriver

@pytest.fixture(scope="function")
def driver():
    options = webdriver.FirefoxOptions()
#   options.add_argument("--headless")  # Запуск в headless-режиме
    driver = webdriver.Firefox(options=options)
    yield driver
    driver.quit()