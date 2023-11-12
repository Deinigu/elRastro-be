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