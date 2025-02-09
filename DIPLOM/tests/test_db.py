import pytest
import allure
import sqlite3

@pytest.fixture(scope="module")
def db_connection():
    conn = sqlite3.connect(":memory:") 
    yield conn
    conn.close()

@allure.feature("Работа с базой данных")
@allure.story("Проверка добавления записей в БД")
def test_add_record_to_db(db_connection):
    cursor = db_connection.cursor()
    
    with allure.step("Создание таблицы в БД"):
        cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
    
    with allure.step("Добавление записи в таблицу"):
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Test User", "test@example.com"))
        db_connection.commit()
    
    with allure.step("Проверка наличия записи в таблице"):
        cursor.execute("SELECT * FROM users WHERE name = ?", ("Test User",))
        user = cursor.fetchone()
        assert user is not None, "Запись не была добавлена в БД"
        assert user[1] == "Test User", "Имя пользователя не совпадает"