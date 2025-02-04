import gevent.monkey
gevent.monkey.patch_all()

from locust import HttpUser, task, between, LoadTestShape
import allure

# Нагрузочное тестирование
class WebsiteUser(HttpUser):
    wait_time = between(1, 2)

    @task
    @allure.step("Загрузка главной страницы")
    def load_home_page(self):
        self.client.get("https://ormea.pl/")

# Стресс-тестирование
class StressedShape(LoadTestShape):
    def tick(self):
        run_time = self.get_run_time()
        if run_time < 600:
            return (run_time, run_time)
        return None

class StressedUser(HttpUser):
    wait_time = between(1, 2)

    @task
    @allure.step("Загрузка главной страницы")
    def load_home_page(self):
        self.client.get("https://ormea.pl/")
