# BookWorms
BookWorms - это социальная сеть, где каждый может поделиться своей историей и 
узнать мнения других пользователей. 

## Как запустить проект:
Клонировать репозиторий и перейти в каталог:

```bash
cd yatube_api\
```

Cоздать и активировать виртуальное окружение:

```bash
python3 -m venv env
source env/bin/activate
```
Установить зависимости из файла requirements.txt:
```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
Выполнить миграции:
```bash
python3 manage.py migrate
```
Запустить проект:
```bash
python3 manage.py runserver
```
