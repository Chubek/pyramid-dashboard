#!/bin/sh
exec gunicorn -b :5000 --access-logfile - --timeout 5000 --error-logfile - app:app