import pytest
from selenium import webdriver
from pages.branze_page import BranzePage
from pages.home_page import HomePage

@pytest.fixture(scope="function")
def driver():
    options = webdriver.ChromeOptions()
#   options.add_argument("--headless")  # Запуск в headless-режиме
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()
    
@pytest.fixture
def setup(driver):
    home_page = HomePage(driver)
    home_page.open("https://ormea.pl/")
    yield home_page 