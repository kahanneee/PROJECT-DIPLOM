import pytest
from selenium import webdriver
from pages.branze_page import BranzePage
from pages.home_page import HomePage
from pages.uslugi_page import UslugiPage
 
@pytest.fixture(scope="function")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()
    
@pytest.fixture
def home_setup(driver):
    home_page = HomePage(driver)
    home_page.open("https://ormea.pl/")
    yield home_page 
    
@pytest.fixture
def branze_setup(driver):
    branze_page = BranzePage(driver)
    branze_page.open("https://ormea.pl/branze/")
    yield branze_page
    
@pytest.fixture
def uslugi_setup(driver):
    uslugi_page = UslugiPage(driver)
    uslugi_page.open("https://ormea.pl/uslugi/")
    yield uslugi_page 
    
@pytest.fixture(scope="session")
def driver_stability():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--remote-debugging-port=9222")  
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()