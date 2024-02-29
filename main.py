import requests
import psycopg2
from datetime import date, timedelta
from dotenv import load_dotenv
import os

# Загрузка переменных среды из файла .env
load_dotenv()

# Подключение к базе данных PostgreSQL
try:
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cur = conn.cursor()

    # Проверяем, есть ли записи за сегодняшний день в базе данных
    today = date.today()
    cur.execute("SELECT COUNT(*) FROM tickets_retro WHERE date = %s", (today,))
    count = cur.fetchone()[0]

    # Если нет записей за сегодняшний день, выполняем ваш код
    if count == 0:
        # Ваш код здесь 
        url = "https://jira.o3.ru/rest/api/2/search/"
        headers = {
            "Authorization": f"Bearer {os.getenv('JIRA_API_TOKEN')}"
        }

        params = {
            "jql": f'project = sd911 AND "Группа исполнителей" = TS_MSK_city_team AND "Customer Request Type" not in ("(Офис)Организация нового рабочего места", "Возврат оборудования в ИТ") AND status was in ("В работе") ON "{today.strftime("%Y-%m-%d")} 01:00"',
            "maxResults": 0,
            "fields": "total"
        }

        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            total_tickets = data["total"]

            insert_query = "INSERT INTO tickets_retro (date, total) VALUES (%s, %s);"
            cur.execute(insert_query, (today, total_tickets))
            conn.commit()

            print("Total number of tickets:", total_tickets)
            print("Date:", today)
            print("Stored in the database")
        else:
            print("Request failed with status code:", response.status_code)

except (Exception, psycopg2.DatabaseError) as error:
    print("Error:", error)

finally:
    if cur:
        cur.close()
    if conn:
        conn.close()
