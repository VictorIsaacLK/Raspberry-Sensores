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
        
           
    def update_all_documents(self, db_name, coll_name, new_docs):
        try:
            db = self.client[db_name]
            coll = db[coll_name]
            coll.delete_many({})
            coll.insert_many(new_docs)
        except Exception:
            print("No se pudo establecer una conexión a MongoDB se recomineda restablecer su conexion ")
            
    def hacer_find(self):
        try:
            db = self.client['Tienda']
            collection = db['Productos']
                    
            result = collection.find()
            for doc in result:
                print(doc)
        except Exception:
            return False
        
        
    def guardar_en_mongo(self, db_name, coll_name, lista, nombre_json, nombre_temp_json):
        try:
            super().enviarDiccionarioYAlmacenamientoJson(nombre_json, lista)
            db = self.client[db_name]
            collection = db[coll_name]
            collection.delete_many({})
            collection.insert_many(lista)
        except Exception:
            super().enviarDiccionarioYAlmacenamientoJson(nombre_temp_json, lista)
            return False
            
    def cerrar_conexion(self):
        self.client.close()
        
    def borrar_json(self, nombre_json):
        if path.exists(nombre_json):
            remove(nombre_json)
            
        
            
        
        