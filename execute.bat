@echo off

:: Install requirements
pip install -r requirements.txt

:: Run migrations and Django servers
python usuarios\manage.py migrate
start cmd /k python usuarios\manage.py runserver 8000

python productos\manage.py migrate
start cmd /k python productos\manage.py runserver 8001

python pujas\manage.py migrate
start cmd /k python pujas\manage.py runserver 8002

python huellaDeCarbono\manage.py migrate
start cmd /k python huellaDeCarbono\manage.py runserver 8003

python horaLocal\manage.py migrate
start cmd /k python horaLocal\manage.py runserver 8004

python cambiomoneda\manage.py migrate
start cmd /k python cambiomoneda\manage.py runserver 8005