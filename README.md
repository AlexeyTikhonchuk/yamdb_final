
![example workflow](https://github.com/AlexeyTikhonchuk/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

https://158.160.15.197/

# Проект YaMDb
### Описание
Проект YaMDb собирает отзывы пользователей на различные произведения.

В проекте реализован REST API для YaMDb, позволяющий получать 
информацию об отзывах пользователей на произведения, 
которые делятся на категории и жанры. 

Пользователи могут оставлять комментарии к отзывам.

## Запуск проекта на локальной машине:
Клонировать репозиторий:
`https://github.com/alexeytikhonchuk/yamdb_final.git`
В директории infra файл .env заполнить своими данными:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY='секретный ключ Django'
```
Создать и запустить контейнеры Docker, выполнить команду в терминале из папки infra:
```
docker-compose up -d
```
После успешной сборки выполнить миграции:
```
docker-compose exec backend python manage.py migrate
```
Создать суперпользователя:
```
docker-compose exec backend python manage.py createsuperuser
```
Собрать статику:
```
docker-compose exec backend python manage.py collectstatic --noinput
```

### Технологии
- python
- django
- docker

## Примеры запросов
### Получение списка произведений
Для получения списка всех произведений необходимо отправить 
Get-запрос на адрес `http://127.0.0.1:8000/api/v1/titles/`.
При помощи параметров `limit` и `offset` можно настроить размер
и область выдачи

Пример ответа:
```
{
    "count": 32,
    "next": "http://127.0.0.1:8000/api/v1/titles/?limit=3&offset=3",
    "previous": null,
    "results": [
        {
            "id": 3,
            "category": {
                "name": "Фильм",
                "slug": "movie"
            },
            "genre": [
                {
                    "name": "Драма",
                    "slug": "drama"
                }
            ],
            "rating": 7,
            "name": "12 разгневанных мужчин",
            "year": 1957,
            "description": ""
        },
        {
            "id": 30,
            "category": {
                "name": "Музыка",
                "slug": "music"
            },
            "genre": [
                {
                    "name": "Рок",
                    "slug": "rock"
                }
            ],
            "rating": 10,
            "name": "Deep Purple — Smoke on the Water",
            "year": 1971,
            "description": ""
        },
        {
            "id": 29,
            "category": {
                "name": "Музыка",
                "slug": "music"
            },
            "genre": [
                {
                    "name": "Rock-n-roll",
                    "slug": "rock-n-roll"
                }
            ],
            "rating": 10,
            "name": "Elvis Presley - Blue Suede Shoes",
            "year": 1955,
            "description": ""
        }
    ]    
}
```
### Регистрация
Для регистрации нового пользователя
POST-запрос на адрес `http://127.0.0.1:8000/api/v1/auth/signup/`.
В запросе указать поля `email` и `username`.

```
{
"email": "string",
"username": "string"
}
```
### Получение токена
Для получения токена необходимо отправить 
POST-запрос на адрес `http://127.0.0.1:8000/api/v1/auth/token/`.
В запросе указать поля `confirmation_code` и `username`.

```
{
"username": "string",
"confirmation_code": "string"
}
```
### Автор
Алексей Тихончук
