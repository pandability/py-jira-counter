FROM python:3.9

# Установка рабочей директории
WORKDIR /app

# Копирование всех файлов в контейнер
COPY . /app

# Установка зависимостей Python
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Установка PostgreSQL
RUN apt-get update && apt-get install -y postgresql
RUN service postgresql start

# Создание базы данных и пользователя (пример)
RUN su - postgres -c "psql -c 'CREATE DATABASE postgres;'"
RUN su - postgres -c "psql -c 'CREATE USER postgres WITH PASSWORD '\''Vbvbrf33'\'';'"
RUN su - postgres -c "psql -c 'GRANT ALL PRIVILEGES ON DATABASE postgres TO postgres;'"

# Подключение к базе данных и создание таблицы
RUN su - postgres -c "psql -d postgres -c 'CREATE TABLE tickets_retro (id SERIAL PRIMARY KEY, date DATE, total INT);'"

# Запуск вашего приложения
CMD ["python", "main.py"]