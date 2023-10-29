from django.db import models

# Create your models here.
import pymongo
#connect_string = 'mongodb+srv://<username>:<password>@<atlas cluster>/<myFirstDatabase>?retryWrites=true&w=majority' 

from django.conf import settings
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
for r in med_details:
    print(r["NombreUsuario"])
# Update one document
update_data = collection_name.update_one({'_id':'RR000123456'}, {'$set':{'NombreUsuario':'Paracetamol 500'}})

# Delete one document
delete_data = collection_name.delete_one({'_id':'RR000123456'})