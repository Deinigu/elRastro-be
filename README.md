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
### Dependencias
Una vez activado el virtual environment pasamos a instalar las dependencias con el siguiente comando:
  
    pip install -r requirements.txt

### Ejecutar el proyecto
Ahora podemos ejecutar el proyecto para probar todas sus funciones, tendremos que ejectuar cada microservicio en un puerto distinto si queremos ejecutarlos todos a la vez
   ```
   python manage.py runserver 127.0.0.1:PUERTO
   ```

# Como crear un proyecto en Django (y aplicación)

1. Crear el proyecto
      ```
      django-admin startproject nombreDelProyecto
      ```

2. Crear la aplicación
      ```
      cd nombreDelProyecto
      python manage.py startapp nombreDeLaAplicación
      ```

3. Añadir la aplicación a INSTALLED_APPS en settings.py (y otras que usemos)
   ```
   INSTALLED_APPS = [
    'rest_framework',
    'elrastroapp',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
   ]
   ```

4. Crear un serializer
   
6. Crear un urls.py en la aplicación
   ```
   from django.urls import path
   from elrastroapp import views
   
   urlpatterns = [
   
       # PUJAS
       path('api/pujas', views.pujas_list_view),
   ]
   ```
8. Añadir las urls de la aplicación al urls.py del proyecto
   ```
   from django.contrib import admin
   from django.urls import path, include
   
   urlpatterns = [
       path('admin/', admin.site.urls),
       path('', include('elrastroapp.urls')),
   ]
   ```
9. Crear las views importando la base de datos y colección
   ```
   # ----------------------------------------  VISTAS DE LA APLICACIÓN ------------------------------
   # Conexión a la base de datos MongoDB
   my_client = pymongo.MongoClient('mongodb+srv://usuario:usuario@elrastrodb.oqjmaaw.mongodb.net/')
   
   # Nombre de la base de datos
   dbname = my_client['ElRastro']
   
   # Colecciones
   collection_usuarios = dbname["usuarios"]
   ```

   
