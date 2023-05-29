# TP
Проект для курса "Технологии программирования"
## Запуск
Для запуска необходимо установить Python 3.10.x и пакетный менеджер pip.
Создание виртуального окружения:
```
python -m venv venv 
source venv/bin/activate
```
Для отключения виртуального окружения:
```
deactivate
```
Далее установить зависимости:
```
pip install -r requirements.txt
```
Создание миграций:
```
python manage.py make migrations
python manage.py migrate
```
Запуск сервера:
```
python manage.py runserver
```

## Авторы
* **Юрий Мирончик** - [Yura192c]()
