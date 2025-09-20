web: gunicorn proavocado.wsgi:application
python manage.py migrate && python manage.py collectstatic --noinput && gunicorn proavocado.wsgi:application