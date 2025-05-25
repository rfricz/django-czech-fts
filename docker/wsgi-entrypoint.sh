#!/bin/sh

python manage.py migrate &&
python manage.py collectstatic --no-input &&
rm -f /run/gunicorn.sock &&
exec gunicorn
