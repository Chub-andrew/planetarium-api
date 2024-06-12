# Planetarium API

API service for planetarium management on DRF

Install PostgresSQL and create db

git clone https://github.com/Chub-andrew/planetarium-api.git

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