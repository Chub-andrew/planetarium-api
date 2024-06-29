# Planetarium API

API service for planetarium management on DRF

Install PostgresSQL and create db

git clone https://github.com/Chub-andrew/planetarium-api.git

This project uses environment variables for configuration. To set them up, follow these steps:
* Rename the `.env.sample` file to `.env`.
* Fill in the values for each variable based on your environment or project requirements.

#### Available Environment Variables

- **POSTGRES_PASSWORD**: Password for PostgreSQL database.
- **POSTGRES_USER**: Username for PostgreSQL database.
- **POSTGRES_DB**: Database name for PostgreSQL.
- **POSTGRES_HOST**: Hostname for PostgreSQL server.
- **POSTGRES_PORT**: Port number for PostgreSQL server (default is 5432).
- **TELEGRAM_TOKEN**: Token for accessing the Telegram API.

cd planetarium_API

python -m venv venv

source venv/scripts/activate

pip install -re requirements.txt

python manage.py migrate

# Run with docker

docker-compose build
docker-compose up

# Getting access
* create user via /api/user/register
* get access token via /api/user/token
![Screenshot_1.png](media/Screenshot_1.png)
![Screenshot_2.png](media/Screenshot_2.png)
![ScreenshotTelegram.png](media/ScreenshotTelegram.png)