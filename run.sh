#!/bin/sh

nohup python manage.py runserver 0.0.0.0:1338 > log &
