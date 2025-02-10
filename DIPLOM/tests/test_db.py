import pytest
import allure
import sqlite3

@pytest.fixture(scope="module")
def db_connection():
    conn = sqlite3.connect(":memory:") 
    yield conn
    conn.close()

@allure.feature("Работа с базой данных")
@allure.story("Проверка таблицы контактов")
def test_create_contacts_table(db_connection):
    cursor = db_connection.cursor()
    
    with allure.step("Создание таблицы контактов"):
        cursor.execute("""
            CREATE TABLE contacts (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                address TEXT NOT NULL
            )
        """)
        db_connection.commit()
    
    with allure.step("Проверка создания таблицы"):
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='contacts'")
        table = cursor.fetchone()
        assert table is not None, "Таблица 'contacts' не была создана"

@allure.feature("Работа с базой данных")
@allure.story("Проверка добавления записи в таблицу контактов")
def test_add_contact(db_connection):
    cursor = db_connection.cursor()
    
    with allure.step("Добавление записи в таблицу контактов"):
        cursor.execute("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)",
                       ("Aryna Lasminskaya", "+48728490702", "a.lasm9117@gmail.com", "Malawskiego 7"))
        db_connection.commit()
    
    with allure.step("Проверка добавления записи"):
        cursor.execute("SELECT * FROM contacts WHERE name = ?", ("Aryna Lasminskaya",))
        contact = cursor.fetchone()
        assert contact is not None, "Запись не была добавлена в таблицу 'contacts'"
        assert contact[1] == "Aryna Lasminskaya", "Имя контакта не совпадает"
