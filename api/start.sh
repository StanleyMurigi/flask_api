#!/bin/bash
python manage.py migrate
gunicorn myproject.wsgi

