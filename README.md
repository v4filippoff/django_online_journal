# django_online_journal

Блог с постами, комментариями и регистрацией пользователей

## Установка

Склонируйте репозиторий и перейдите в нужную директорию
```sh
$ git clone https://github.com/v4filippoff/django_online_journal.git
$ cd django_online_journal
```

Создайте виртуальное окружение для пакетов Python и активируйте его
```sh
$ python -m venv venv
$ source venv/bin/activate
```

Установите все зависимости
```sh
$ pip install -r requirements.txt
```

Примените миграции к базе данных
```sh
$ cd django_project/
$ python manage.py migrate
```

Запустите локальный сервер
```sh
$ python manage.py runserver
```

Перейдите к `http://localhost:8000/`
