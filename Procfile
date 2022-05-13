release: python manage.py migrate
web: python manage.py collectstatic --no-input; gunicorn carzone.wsgi --log-file - --log-level debug
