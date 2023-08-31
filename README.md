# JIRA Ticket Counter

This script connects to a PostgreSQL database, retrieves the total number of tickets from the JIRA API, and stores the total number of tickets, current date, and current time in the database.

## Prerequisites

- PostgreSQL database.
- Python 3 and pip installed.
- JIRA API account with appropriate token.
- Environment variables set in a .env file:
  - `DB_HOST` - PostgreSQL database host
  - `DB_PORT` - PostgreSQL database port
  - `DB_NAME` - PostgreSQL database name
  - `DB_USER` - PostgreSQL database username
  - `DB_PASSWORD` - PostgreSQL database password


## Installation

1. Clone the repository:

```bash
git clone https://github.com/example/jira-ticket-counter.git
cd jira-ticket-counter
```

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

3. Set the environment variables:
- Create a file named `.env` in the project directory and set the following environment variables:
```bash
DB_HOST=<your_database_host>
DB_PORT=<your_database_port>
DB_NAME=<your_database_name>
DB_USER=<your_database_username>
DB_PASSWORD=<your_database_password>
```

4. Update the JIRA API token:
- In the `main.py` file, replace `Bearer ************************HYPmCL` with your `JIRA API` token.

## Usage

Run the script by executing the following command:

```bash
python main.py
```

## Contributing

Contributions are welcome! Please feel free to create a pull request.


