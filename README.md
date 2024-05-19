# Веб-приложение для публикации постов «Blogicum»

## _Описание проекта:_

#### **_*Blogicum*_ - блог, каркас для социальной сети.**


### _Возможности проекта:_
* регистрация пользователей;
* возможность добавления/редактирования/удаления своих публикаций;
* просмотр публикаций других пользователей;
* возможность добавления комментариев к публикациям;
* добавление к публикациям фото;
* просмотр публикаций в разрезе категорий и локаций.

### _Запуск проекта:_
- Склонировать репозиторий:
```
git clone git@github.com:V1olenceDev/django_sprint4.git
```
- Создать и активировать виртуальное окружение:
```
python -m venv venv
. venv/Scripts/activate
```
- Обновить pip:
```
python -m pip install --upgrade pip
```
- Установить библиотеки:
```
pip install -r requirements.txt
```
- Выполнить миграции:
```
python blogicum/manage.py migrate
```
- Загрузить фикстуры DB:
```
python blogicum/manage.py loaddata db.json
```
- Создать суперпользователя:
```
python blogicum/manage.py createsuperuser
```
- Запустить сервер django:
```
python blogicum/manage.py runserver
```
##
### Автор
[Гаспарян Валерий Гургенович](https://github.com/V1olenceDev)
##
