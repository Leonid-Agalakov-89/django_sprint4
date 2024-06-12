## О проекте:

Веб-приложение в виде блога, на котором пользователь может создать свою страницу и публиковать на ней посты. Для каждого поста нужно указать категорию, а также опционально локацию, с которой связан пост. Пользователь может перейти на страницу любой категории и увидеть все посты, которые к ней относятся. Пользователи могут заходить на чужие страницы, читать и комментировать чужие посты.


# Установка:

1) Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Leonid-Agalakov-89/django_sprint4.git
```

```
cd django_sprint4
```

2) Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source env/bin/activate
```

3) Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

4) Выполнить миграции:

```
python manage.py makemigrations
```

```
python manage.py migrate
```

5) Запустить проект:

```
python manage.py runserver
```


## Технологии:

Backend
* Django
* SQLite3

Frontend
* HTML
* django_bootstrap5


## Об авторе:
Леонид Агалаков - python backend developer.
`https://github.com/Leonid-Agalakov-89`
