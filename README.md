## Инструкции по установке и запуску проекта

- Скачать [Докер](https://docs.docker.com/engine/install/)
- Загрузить проект с помощью команды `git clone `
- Запустить проект с помощью `docker compose up --abort-on-container-exit --exit-code-from app`

*В проекте изначально пустая база данных*

**Для проверки get_form запустите юнит тесты с помощью команды**:

`docker compose -f compose.test.yaml up --abort-on-container-exit --exit-code-from app`