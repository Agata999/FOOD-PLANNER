# Zaplanuj Jedzonko - Scrum
> A web application to plan meals created with Django and Scrum methodology 

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Status](#status)

## General info
Scrum project created with Django. My part of project: list of recipes, creating a possibility to add, edit, delete, find a recipe

## Technologies
* Python - version 3.6
* Django - version 2.2.4
* PostgreSQL - version 10.10

## Setup
* Clone git repository
* Create virtualenv `virtualenv -p python3 venv`
* Activate virtualenv `source venv/bin/activate`
* Install requirements `pip install -r requirements.txt`
* Setup psql database called `jedzonko_db`
* Change psql user and password to yours
* `python manage.py migrate`
* `python manage.py runserver`

## Status
Project is: _finished_
