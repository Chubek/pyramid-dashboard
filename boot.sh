#!/bin/sh
exec gunicorn -b :8000 --access-logfile - --timeout 10000 --error-logfile - dashboard:server