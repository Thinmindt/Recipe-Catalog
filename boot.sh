#!/bin/bash
while true; do
  flask db upgrade
  if flask db upgrade; then
    break
  fi
  echo Upgrade command failed, retrying in 5 seconds...
  sleep 5
done
if [ $FLASK_ENV = production ]; then
  exec gunicorn -b :5000 --access-logfile - --error-logfile - recipe_catalog:app
else
  exec flask run -h 0.0.0.0 -p 5000
fi