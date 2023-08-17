#1/bin.sh

flash db upgrade

exec gunicorn --bind 0.0.0.0:80 "app:create_app()"