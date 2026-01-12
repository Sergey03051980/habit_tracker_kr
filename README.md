# Habit Tracker - Django API с Docker и CI/CD

Проект для отслеживания привычек с полной автоматизацией развертывания.

## 🚀 Быстрый запуск

### С Docker:
```bash
docker-compose -f docker-compose.dev.yml up --build

Без Docker:
bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
🤖 CI/CD
Тесты запускаются при каждом push

Деплой на Yandex Cloud при push в main

Конфиги в .github/workflows/

🐳 Docker
Все сервисы в контейнерах

2 конфигурации: dev и prod

Готово к деплою на сервер

🌐 Деплой
Создать VM в Yandex Cloud

Запустить scripts/setup_server.sh

Добавить Secrets в GitHub

Сделать push в main


---
Проект готов для сдачи домашнего задания.
