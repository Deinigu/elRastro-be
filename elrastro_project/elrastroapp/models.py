from django.db import models
from django.contrib.postgres.fields import ArrayField

# --------------------------- NO SE USAN MODELOS AL UTILIZAR MONGODB COMO BASE DE DATOS NO RELACIONAL PARA EL BACKEND -----------------
'''
# Create your models here.
import pymongo
#connect_string = 'mongodb+srv://<username>:<password>@<atlas cluster>/<myFirstDatabase>?retryWrites=true&w=majority' 

from django.conf import settings
class Usuario(models.Model):
    _id = models.CharField(max_length=24, primary_key=True)
    correo = models.EmailField(unique=True)
    fotoURL = models.URLField()
    listaConver = models.ManyToManyField('Conversacion')
    productosVenta = models.ManyToManyField('Producto')  
    reputacion = models.DecimalField(max_digits=3, decimal_places=1)
    telefono = models.CharField(max_length=20)
    vivienda = models.CharField(max_length=100)
    contrasenya = models.CharField(max_length=100)
    nombreUsuario = models.CharField(max_length=50)

    def __str__(self):
        return str(self._id)
    
    class Meta:
        db_table = 'usuarios'

class Producto(models.Model):
    _id = models.CharField(max_length=24, primary_key=True)  # Utiliza CharField como clave primaria
    Nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateField()
    fotoURL = models.URLField()
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    tags = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=100)
    vendedor = models.CharField(max_length=24)
    cierre = models.DateField()
    pujas = ArrayField(base_field=models.CharField(max_length=24))

    def __str__(self):
        return self.Nombre

    class Meta:
        db_table = 'productos'

class Puja(models.Model):
    _id = models.CharField(max_length=24, primary_key=True)  # Utiliza CharField como clave primaria
    pujador = models.CharField(max_length=24)
    valor = models.DecimalField(max_digits=6, decimal_places=2)
    fecha = models.DateField()
    producto = models.CharField(max_length=24)
    def __str__(self):
        return f"Puja de {self.pujador} en {self.producto} - Valor: {self.valor}"
    class Meta:
        db_table = 'pujas'

class Conversacion(models.Model):
    _id = models.CharField(max_length=24, primary_key=True)  # Utiliza CharField como clave primaria
    remitente = models.CharField(max_length=24)
    destinatario = models.CharField(max_length=24)    #Creo que puedes usar los related_name para hacer algo tipo conversaciones_enviadas = usuario.conversaciones_enviadas.all()
    n_mensajes = models.PositiveIntegerField() 
    ultimo_mensaje = models.TextField()

    def __str__(self):
        return f'Conversación entre {self.remitente.nombreUsuario} y {self.destinatario.nombreUsuario}'
    class Meta:
        db_table = 'conversaciones'

my_client = pymongo.MongoClient('mongodb+srv://usuario:usuario@elrastrodb.oqjmaaw.mongodb.net/')

# First define the database name
dbname = my_client['ElRastro']

# Now get/create collection name (remember that you will see the database in your mongodb cluster only after you create a collection
collection_name = dbname["usuarios"]

#let's create two documents
ejemplo_1 = {
    "NombreUsuario": "Lucas1234",
    "correo": "luca@gmail.com",
    "fotoURL": "urlexample1",
    "listaConver": "listac1",
    "productosVenta": "listap1",
    "reputacion": 4,
    "telefono": "123321122",
    "vivienda": "Inglaterra"
}
ejemplo_2 = {
    "NombreUsuario": "Lucas4321",
    "correo": "luca@gmail.com",
    "fotoURL": "urlexample1",
    "listaConver": "listac1",
    "productosVenta": "listap1",
    "reputacion": 4,
    "telefono": "123321122",
    "vivienda": "Corea del Sur"
}
# Insert the documents
collection_name.insert_many([ejemplo_1, ejemplo_2])
# Check the count
count = collection_name.count()
print(count)

# Read the documents
med_details = collection_name.find({})
# Print on the terminal
# for r in med_details:
#   print(r["NombreUsuario"])
# Update one document
update_data = collection_name.update_one({'_id':'RR000123456'}, {'$set':{'NombreUsuario':'Paracetamol 500'}})

# Delete one document
delete_data = collection_name.delete_one({'_id':'RR000123456'})
'''