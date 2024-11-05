# API для Yamdb

## Описание
Проект YaMDb собирает отзывы пользователей на различные произведения.
## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/EmilDragunov/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```