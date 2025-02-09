Дипломный проект, который тестирует сайт https://ormea.pl/ на использование сторонним пользователем. 

Ссылка на репозиторий. https://github.com/kahanneee/PROJECT-DIPLOM

Структура проекта:
├──DIPLOM
├──├── pages
├──├──├──__init__.py
├──├──├──base_page.py
├──├──├──branze_page.py
├──├──├──home_page.py
├──├──├──uslugi_page.py
├──├── tests
├──├──├──__init__.py
├──├──├──test_api.py - тесты, связанные с API
├──├──├──test_availability.py -тесты на проверку использования сайта людьми, с ограниченными возможностями 
├──├──├──test_branze_page.py - тест на проверку страницы Branże
├──├──├──test_db.py -тест, связанный с базой данных
├──├──├──test_docker.py - тест проверяет запуск и состояние контейнеров Docker.
├──├──├──test_home_page.py  тесты на проверку стартовой страницы
├──├──├──test_stability.py - тесты на проверку производительности и уйстойчивости 
├──├──├──test_perfomance.py - тесты на проверку работы сайта, в разных режимах
├──├──├──test_responsiveness.py - тесты на проверку адапнтивности сайта на разных устройствах
├──├──├──test_uslugi.py - тесты на проверку страницы Uslugi
├──├──├──test_vulnerability.py - тесты на проверку устойчивости сайта к различным атакам
├──├──.gitignore
├──├──accessibility_results.json
├──├──locustfile.py - дополнительные зависимости для проверки сайта с нагрузками 
├──├──pytest.ini 
├──├──README.md
├──├──requirements.txt - зависимости 
