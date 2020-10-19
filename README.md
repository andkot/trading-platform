# trading-platform
Trading platform back-end

Run app on docker:
linux commands:

sudo docker build .
sudo docker-compose build
sudo docker-compose up -d --build
sudo docker-compose exec trading-platform python src/manage.py makemigrations --noinput
sudo docker-compose exec trading-platform python src/manage.py migrate --noinput

