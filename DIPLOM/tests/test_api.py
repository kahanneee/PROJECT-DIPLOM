import requests
import allure

@allure.feature("Работа с API")
@allure.story("Проверка API пользователей")
def test_users_api():
    url = "https://jsonplaceholder.typicode.com/users"
    
    with allure.step("Отправка GET запроса к API"):
        response = requests.get(url)
        assert response.status_code == 200, "API запрос завершился с ошибкой"

    with allure.step("Проверка структуры данных"):
        users = response.json()
        assert len(users) > 0, "Список пользователей пуст"
        assert "id" in users[0] and "name" in users[0], "Структура данных пользователей неверная"

@allure.feature("Работа с API")
@allure.story("Создание пользователя через API")
def test_create_user_api():
    url = "https://jsonplaceholder.typicode.com/users"
    new_user = {
        "name": "Test User",
        "username": "testuser",
        "email": "testuser@example.com"
    }

    with allure.step("Отправка POST запроса для создания пользователя"):
        response = requests.post(url, json=new_user)
        assert response.status_code == 201, "Создание пользователя завершилось с ошибкой"
        user = response.json()
        assert user["name"] == new_user["name"], "Имя созданного пользователя не соответствует"