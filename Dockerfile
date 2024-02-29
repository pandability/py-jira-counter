FROM python:3.9

# Установка рабочей директории
WORKDIR /app

# Копирование всех файлов в контейнер
COPY . /app

# Установка зависимостей Python
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Добавление скрипта для запуска ежедневной задачи
COPY run_daily.sh /app/run_daily.sh
RUN chmod +x /app/run_daily.sh

# Добавление cron-задачи для запуска скрипта
RUN echo "0 3 * * * /app/run_daily.sh" >> /etc/crontab

# Запуск cron в фоновом режиме
CMD ["cron", "-f"]

# Создание базы данных и таблицы
RUN apt-get update && apt-get install -y postgresql-client

RUN PGPASSWORD=passwd psql -h postgres_jira -U postgres -c "CREATE DATABASE IF NOT EXISTS postgres;"
RUN PGPASSWORD=passwd psql -h postgres_jira -U postgres -d postgres -c "CREATE TABLE IF NOT EXISTS tickets_retro (id SERIAL PRIMARY KEY, date DATE, total INT);"
