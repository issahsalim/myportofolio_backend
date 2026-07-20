web: python manage.py migrate && python seed_data.py && python manage.py collectstatic --noinput && gunicorn core.wsgi:application
