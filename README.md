# Django API для управления постами, комментариями, группами и подписками

## Описание

Этот проект представляет собой REST API, созданный на базе Django и Django REST Framework. API предоставляет функционал для управления:

- Постами (создание, редактирование, удаление);
- Комментариями к постам;
- Группами;
- Подписками на других пользователей.

API поддерживает авторизацию пользователей и предоставляет доступ только к разрешённым действиям. В основе работы лежат модели `Post`, `Group`, `Comment` и `Follow`.

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/IvanMareev/api_final_yatube.git
   ```

2. Перейдите в директорию проекта:

   ```bash
   cd api_final_yatube
   ```

3. Установите виртуальное окружение и активируйте его:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Для Windows: venv\Scripts\activate
   ```

4. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

5. Выполните миграции базы данных:

   ```bash
   python manage.py migrate
   ```

6. Создайте суперпользователя для доступа к админ-панели:

   ```bash
   python manage.py createsuperuser
   ```

7. Запустите локальный сервер разработки:

   ```bash
   python manage.py runserver
   ```

8. API будет доступно по адресу: `http://127.0.0.1:8000/`

## Примеры запросов

### Работа с постами

#### Получение списка постов

```http
GET api/v1/posts/
```

Пример ответа:
```json
[
  {
    "id": 1,
    "author": "user1",
    "text": "Пример поста",
    "created": "2024-01-01T12:00:00Z"
  }
]
```

#### Создание поста

```http
POST api/v1/posts/
```

Тело запроса:
```json
{
  "text": "Новый пост"
}
```

### Работа с комментариями

#### Получение комментариев к посту

```http
GET api/v1/posts/{post_id}/comments/
```

Пример ответа:
```json
[
  {
    "id": 1,
    "author": "user2",
    "text": "Пример комментария",
    "created": "2024-01-01T13:00:00Z"
  }
]
```

#### Создание комментария

```http
POST api/v1/posts/{post_id}/comments/
```

Тело запроса:
```json
{
  "text": "Новый комментарий"
}
```

### Работа с подписками

#### Подписка на пользователя

```http
POST api/v1/follow/
```

Тело запроса:
```json
{
  "following": "user3"
}
```

Пример ответа:
```json
{
  "user": "user1",
  "following": "user3"
}
```

## Авторизация через Djoser

Для управления аутентификацией и авторизацией используется библиотека [Djoser](https://djoser.readthedocs.io/). Она предоставляет готовые эндпоинты для регистрации, входа в систему, выхода и управления пользователями.

### Примеры запросов к Djoser

#### Регистрация пользователя

```http
POST api/v1/auth/users/
```

Тело запроса:
```json
{
  "username": "newuser",
  "password": "securepassword",
  "email": "newuser@example.com"
}
```

#### Получение токена для аутентификации

```http
POST api/v1/auth/token/login/
```

Тело запроса:
```json
{
  "username": "newuser",
  "password": "securepassword"
}
```

Пример ответа:
```json
{
  "auth_token": "123abc456def"
}
```

#### Выход из системы

```http
POST api/v1/auth/token/logout/
```

Запрос должен содержать токен в заголовке:
```http
Authorization: Token 123abc456def
```



