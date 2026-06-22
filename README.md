# django_sprint4

# 1 Виртуальное окружение

1. Создание
   ```bash
   python -m venv venv
   ```

2. Активация
   ```bash
   source venv/Scripts/activate
   ```

3. Установка зависимостей
   ```bash
   pip install -r requirements.txt
   ```

# 2 Миграции

1. Перейти в папку blogicum
   ```bash
   cd blogicum
   ```

2. Создание миграций
   ```bash
   python manage.py makemigrations
   ```

3. Применение миграций
   ```bash
   python manage.py migrate
   ```

# 3 Запуск

1. Заполнение демо данными
   ```bash
   python manage.py loaddata db.json
   ```

2. Запустить сервер
   ```bash
   python manage.py runserver
   ```
