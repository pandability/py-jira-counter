import requests  # Import the requests library for making HTTP requests
import psycopg2  # Import the psycopg2 library for connecting to PostgreSQL
from datetime import date, datetime  # Import the date and datetime classes from the datetime module
from dotenv import load_dotenv  # Import the load_dotenv function from the dotenv module
import os  # Import the os module for accessing environment variables

# Load variables from .env file
load_dotenv()

try:
    # Connect to the database
    conn = psycopg2.connect(
        # Connection configuration
        host=os.getenv("DB_HOST"),  # Retrieve the "DB_HOST" environment variable
        port=int(os.getenv("DB_PORT")),  # Retrieve the "DB_PORT" environment variable and convert it to an integer
        database=os.getenv("DB_NAME"),  # Retrieve the "DB_NAME" environment variable
        user=os.getenv("DB_USER"),  # Retrieve the "DB_USER" environment variable
        password=os.getenv("DB_PASSWORD")  # Retrieve the "DB_PASSWORD" environment variable
    )
    cur = conn.cursor()  # Create a cursor object to perform database operations

    # Create table if it doesn't exist
    cur.execute('''CREATE TABLE IF NOT EXISTS tickets (
        id SERIAL PRIMARY KEY,
        date DATE,
        time TIME,
        total INT
    )''')

    # Define the URL and parameters for the GET request to the JIRA API
    url = "https://jira.o3.ru/rest/api/2/search"
    params = {
        "jql": 'project = sd911 AND "Группа исполнителей" = TS_MSK_city_team AND "Customer Request Type" not in ("(Офис)Организация нового рабочего места", "Возврат оборудования в ИТ") AND resolution = Unresolved AND status = "В работе"',
        "maxResults": 0,
        "fields": "total"
    }

    headers = {
        "Authorization": "Bearer NzM4MDMzMjkyMjA5OnUjGSamWtzkl9sa0VsAydHYPmCL"
    }

    # Send the GET request to the JIRA API
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:  # Check if the request is successful
        data = response.json()  # Retrieve the response data as JSON
        total_tickets = data["total"]  # Extract the total number of tickets
        current_date = date.today()  # Get the current date
        current_time = datetime.now().time()  # Get the current time

        # Insert the total into the "tickets" table in the database
        insert_query = "INSERT INTO tickets (date, time, total) VALUES (%s, %s, %s);"
        cur.execute(insert_query, (current_date, current_time, total_tickets))
        conn.commit()  # Commit the changes to the database

        # Print the total number of tickets, current date, and current time
        print("Total number of tickets:", total_tickets)
        print("Current date:", current_date)
        print("Current time:", current_time)
        print("Stored in the database")
    else:
        print("Request failed with status code:", response.status_code)

except (Exception, psycopg2.DatabaseError) as error:
    print("Error:", error)

finally:
    # Close the database connection
    if cur:
        cur.close()
    if conn:
        conn.close()
