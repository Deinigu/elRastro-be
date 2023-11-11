@echo off

:: Install requirements
pip install -r requirements.txt

:: Run Django servers
start cmd /k python usuarios\manage.py runserver 8000
start cmd /k python productos\manage.py runserver 8001
start cmd /k python pujas\manage.py runserver 8002
start cmd /k python huellaDeCarbono\manage.py runserver 8003
start cmd /k python horaLocal\manage.py runserver 8004
start cmd /k python cambiomoneda\manage.py runserver 8005