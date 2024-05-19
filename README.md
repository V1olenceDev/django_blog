# Веб-приложение для публикации постов «Blogicum»

> **Blogicum** - это блог, каркас для социальной сети, позволяющий пользователям регистрироваться, добавлять, редактировать и удалять свои публикации, просматривать публикации других пользователей, добавлять комментарии и фотографии к публикациям, а также просматривать публикации по категориям и локациям.

## Технологии проекта

- Python — высокоуровневый язык программирования.
- Django — веб-фреймворк для разработки веб-приложений.
- SQLite — база данных.
- Bootstrap — фреймворк для создания адаптивного веб-дизайна.

### Как запустить проект:

Клонируйте репозиторий и перейдите в него в командной строке:

```
git clone git@github.com:V1olenceDev/django_blog.git
```

```
cd django_blog
```

Cоздайте и активируйте виртуальное окружение:

```
python -m venv venv
```

```
. venv/Scripts/activate
```

Установите зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполните миграции:

```
python blogicum/manage.py migrate
```
Загрузите фикстуры DB:

```
python blogicum/manage.py loaddata db.json
```

Создайте суперпользователя:

```
python blogicum/manage.py createsuperuser
```

Запустите сервер django:

```
python blogicum/manage.py runserver
```

## Автор
[Гаспарян Валерий Гургенович](https://github.com/V1olenceDev)
