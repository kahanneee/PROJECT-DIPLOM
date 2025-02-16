import docker
import allure
import pytest
import requests
from time import sleep

@allure.feature("Работа с Docker")
@allure.story("Запуск и проверка контейнера с сайтом")
def test_run_docker_container():
    try:
        client = docker.from_env()
    except docker.errors.DockerException as e:
        pytest.fail(f"Не удалось подключиться к Docker Daemon: {e}")

    with allure.step("Запуск Docker контейнера с сайтом"):
        try:
            container = client.containers.run("nginx:latest", ports={'80/tcp': 8080}, detach=True)
        except docker.errors.DockerException as e:
            pytest.fail(f"Ошибка при запуске контейнера: {e}")
    
    # Даем контейнеру немного времени для запуска
    sleep(5)

    with allure.step("Проверка состояния контейнера"):
        try:
            container.reload()
            assert container.status == "running", "Контейнер не запущен"
        except docker.errors.DockerException as e:
            pytest.fail(f"Ошибка при проверке состояния контейнера: {e}")

    with allure.step("Отправка запроса к сайту в контейнере"):
        try:
            response = requests.get('http://localhost:8080')
            assert response.status_code == 200, "Не удалось получить доступ к сайту в контейнере"
            assert "<html>" in response.text, "Сайт не возвращает корректное содержимое"
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Ошибка при отправке запроса к контейнеру: {e}")
    
    with allure.step("Остановка и удаление контейнера"):
        try:
            container.stop()
            container.remove()
        except docker.errors.DockerException as e:
            pytest.fail(f"Ошибка при остановке и удалении контейнера: {e}")
