@echo off

python -m venv elRastroEnv

call elRastroEnv\Scripts\activate.bat

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

python conversaciones\manage.py migrate
start cmd /k python conversaciones\manage.py runserver 8006

python valoraciones\manage.py migrate
start cmd /k python valoraciones\manage.py runserver 8007

python imagenes\manage.py migrate
start cmd /k python imagenes\manage.py runserver 8008

python oAuth\manage.py migrate
start cmd /k python oAuth\manage.py runserver 8009