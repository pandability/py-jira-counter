import requests
import psycopg2
from datetime import date, datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

try:
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS tickets_retro (
        id SERIAL PRIMARY KEY,
        date DATE,
        total INT
    )''')

    url = "https://jira.o3.ru/rest/api/2/search/"
    headers = {
        "Authorization": "Bearer NzM4MDMzMjkyMjA5OnUjGSamWtzkl9sa0VsAydHYPmCL"
    }

    current_date = date.today()
    num_day = current_date.day

    for i in range(120):
        params = {
            "jql": 'project = sd911 AND "Группа исполнителей" = TS_MSK_city_team AND "Customer Request Type" not in ("(Офис)Организация нового рабочего места", "Возврат оборудования в ИТ") AND status was in ("В работе") ON \'%s 01:00\'',
            "maxResults": 0,
            "fields": "total"
        }

        previous_date = current_date - timedelta(days=i)
        formatted_date = previous_date.strftime('%Y-%m-%d')

        params["jql"] = params["jql"] % formatted_date
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            total_tickets = data["total"]

            insert_query = "INSERT INTO tickets_retro (date, total) VALUES (%s, %s);"
            cur.execute(insert_query, (str(previous_date), total_tickets))
            conn.commit()

            print("Total number of tickets:", total_tickets)
            print("Previous date:", previous_date)
            print("Stored in the database")
            #  print(previous_date)
            #  print(formatted_date)
            #  print(params["jql"])
        else:
            print("Request failed with status code:", response.status_code)

except (Exception, psycopg2.DatabaseError) as error:
    print("Error:", error)

finally:
    if cur:
        cur.close()
    if conn:
        conn.close()
