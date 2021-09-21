#!/bin/sh
exec gunicorn -b :5000 --access-logfile - --timeout 10000 --error-logfile - app:app