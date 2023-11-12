# elRastro
## Descripción
Aplicación para la asignatura Ingeniería Web.
## Grupo A4
- Calvo Díaz, Fernando
- Colbert Eastgate, Lucas
- López Reduello, Diego
- Moya Castillo, Miguel
- Sánchez Ibáñez, Alba

## Instalación:
### Clonar el repositorio
Clonamos el repositorio con el siguiente comando:
```
git clone https://github.com/Deinigu/elRastro
```
### Virtual Environment
Es recomendable crear un "virtual environment" donde instalar todas las dependencias, para ello seguimos los siguientes pasos:

1. Crear el virtual environment.
   ```
   python -m venv MyEnv
   ```
2. Activarlo.
    ```
    ./MyEnv/Scripts/activate
    ```
### Ejecución automática (Solo Windows)
El archivo executable.bat que hay en el directorio raíz del repositorio realiza la instalación de todas las dependencias, las migraciones necesarias y ejecuta en su correspondientes puertos los microservicios. Es necesario tener los puertos desde el 8000 al 8005 libres. Para ejecutarlo, basta con ejecutar el siguiente comando:
    ```
./executable.bat
    ```
### Ejecución manual
#### Dependencias
Una vez activado el virtual environment pasamos a instalar las dependencias con el siguiente comando:
  ```
    pip install -r requirements.txt
  ```
#### Migraciones
Una vez hecho esto migraremos todas las entidades necesarias de cada microservicio de la base de datos:
```
python usuarios\manage.py migrate
python productos\manage.py migrate
python pujas\manage.py migrate
python huellaDeCarbono\manage.py migrate
python horaLocal\manage.py migrate
python cambiomoneda\manage.py migrate
```
#### Ejecutar el proyecto
Ahora podemos ejecutar el proyecto para probar todas sus funciones, tendremos que ejectuar cada microservicio en un puerto distinto si queremos ejecutarlos todos a la vez
   ```
   python manage.py runserver 127.0.0.1:PUERTO
   ```
La ejecución recomendada de los microservicios con sus respectivos puertos es la siguiente:
```
python usuarios\manage.py runserver 8000
python productos\manage.py runserver 8001
python pujas\manage.py runserver 8002
python huellaDeCarbono\manage.py runserver 8003
python horaLocal\manage.py runserver 8004
python cambiomoneda\manage.py runserver 8005
```
