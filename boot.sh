#!/bin/sh
exec gunicorn -b :5000 --access-logfile - --timeout 999 --error-logfile - app:app