import pymongo
from Lista import lista
from os import remove
from os import path

class MongoDB(lista.Lista):
    def __init__(self):
        super().__init__()
    
    def connect(self, uri):
        try:
            self.client = pymongo.MongoClient(uri)
            print("Conexión exitosa a MongoDB")
            return self.client
        except Exception as e:
            return False      
        
    def guardar_en_mongo(self, db_name, coll_name, lista, nombre_json, nombre_temp_json):
        try:
            super().enviarDiccionarioYAlmacenamientoJson(nombre_json, lista)
            db = self.client[db_name]
            collection = db[coll_name]
            # collection.delete_many({})
            collection.insert_many(lista)
        except Exception:
            super().enviarDiccionarioYAlmacenamientoJson(nombre_temp_json, lista)
            return False
            
    def cerrar_conexion(self):
        self.client.close()
        
    def borrar_json(self, nombre_json):
        if path.exists(nombre_json):
            remove(nombre_json)
            
        
            
        
        