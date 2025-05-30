#!/bin/bash
# start.sh
python manage.py migrate &
python manage.py runserver &
wait -n
exit $?
