import docker
import allure
import pytest

@allure.feature("Работа с Docker")
@allure.story("Запуск и проверка контейнера")
def test_run_docker_container():
    # Дополнительная проверка на наличие Docker Daemon
    try:
        client = docker.from_env()
    except docker.errors.DockerException as e:
        pytest.fail(f"Не удалось подключиться к Docker Daemon: {e}")

    with allure.step("Запуск Docker контейнера"):
        try:
            container = client.containers.run("nginx:latest", detach=True)
        except docker.errors.DockerException as e:
            pytest.fail(f"Ошибка при запуске контейнера: {e}")
    
    with allure.step("Проверка состояния контейнера"):
        try:
            container.reload()
            assert container.status == "running", "Контейнер не запущен"
        except docker.errors.DockerException as e:
            pytest.fail(f"Ошибка при проверке состояния контейнера: {e}")
    
    with allure.step("Остановка и удаление контейнера"):
        try:
            container.stop()
            container.remove()
        except docker.errors.DockerException as e:
            pytest.fail(f"Ошибка при остановке и удалении контейнера: {e}")