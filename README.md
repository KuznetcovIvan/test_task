## Установка и запуск
1. Клонировать репозиторий `https://github.com/KuznetcovIvan/test_task.git`
2. Перейти в корневую директорию проекта `cd test_task`
3. Создать файл с переменными окружения (`.env`)
- образец в [`.env.example`](.env.example)
4. Находясь в корневой директории, выполнить команду  `docker compose up -d --build`
5. Зайти в `backend` контейнер командой `docker compose exec backend bash`
6. Выполнить миграции командой `make migrate`
7. Создать суперпользователя командой `make superuser`
8. Собрать статику для работы админ-панели `make collectstatic`
### Приложение запустится на [http://localhost:8000/](http://localhost:8000/)
- Чтобы остановить запущенный проект, выполните `docker compose down`
- Если нужно также удалить связанные volumes (например, очистить данные БД) `docker compose down -v`
- Чтобы запустить тесты зайдите в `backend` контейнер командой `docker compose exec backend bash` и выполните `make test`
### [Документация API (Swagger)](http://localhost:8000/docs/)
### [Админ-панель](http://localhost:8000/admin/)
### [Скриншоты работы](images/images.md)

### Workflow для CI: линтер и тесты
[![Main workflow](https://github.com/KuznetcovIvan/test_task/actions/workflows/main.yml/badge.svg)](https://github.com/KuznetcovIvan/test_task/actions/workflows/main.yml)

### Для запуска проекта в прод рекомендуется настроить полноценный CI/CD (например, с помощью GitHub Actions или аналогов).  
Помимо `docker-compose.yml` в репозитории можно создать файл `docker-compose.production.yml`, в котором используются уже собранные и отправленные в Docker-registry образы.

### Процесс деплоя в прод может выглядеть так:

1. CI собирает образы для backend, Celery, Nginx и т.д. и пушит их в приватный Docker-репозиторий.
2. На прод-сервер через деплой (SSH/CI/CD) доставляется файл `docker-compose.production.yml`.
3. На сервере рядом с ним создаётся `.env` с боевыми значениями переменных окружения.
4. Приложение поднимается командой:
   `docker compose -f docker-compose.production.yml up -d`
5. Внешний Nginx настроен как reverse-proxy:
принимает входящие HTTP(S)-запросы;
прокидывает их на порт, на котором работает backend (например, gateway-сервис из compose); используется для получения SSL сертификатов (Let's Encrypt/Certbot).