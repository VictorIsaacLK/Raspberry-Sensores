from Mongo import mongo

class InterafazMongoDB():
    def __init__(self, mongoInstancia = mongo.MongoDB()):
        self.mongoInstancia = mongoInstancia

    

    def MongoInterfaz(self):
        print("---------------------------------------------------------------")
        print("----------------------- MONGO INTERFAZ ------------------------")
        print("[1] Conectar a Mongo\n[2] Guardar datos\n[3] Cerrar conexion\n[9] Salida")
        print("---------------------------------------------------------------")

    def conexion(self, url_coneccion):
            conn = self.mongoInstancia.connect(url_coneccion)
            if conn == False:
                print("Error al conectar con la base de datos")
            else:
                print("Conectado con la base de datos")
    
    def subirMongo(self, diccionario):  
        db_name = input("Ingrese el nombre de la base de datos: ")
        coll_name = input("Ingrese el nombre de la colección: ")
        paquete = diccionario
        self.mongoInstancia.update_all_documents(db_name, coll_name, paquete)
        
    def mirarMongo(self):
        self.mongoInstancia.hacerFind()
        
    def guardarDatosEnMongo(self, nombre_json, nombre_json_temporal, db_nombre, collection_nombre, diccionario):
        try: 
            jsontemporal = self.mongoInstancia.cargar_lista_json(nombre_json_temporal)
            if jsontemporal == False:
                print("No existe nada almacenado de manera temporal actualmente")
                se_guardo = self.mongoInstancia.guardar_en_mongo(db_nombre, collection_nombre, diccionario, nombre_json, nombre_json_temporal)
                if se_guardo == False:
                    print("No existe conexion con la base de datos, se han guardado los datos de manera temporal")
                    # return False // este lo puse despues yo, pero veo que no lo necesito porque es en el except donde necesito el false, aqui nada mas me esta avisando que seguardo de manera temporal

                    # De aqui en adelante si exite la conexion, al menos en este if, es cuando no existe archivo temporal, pero si conexion            
                else:
                    print("Se han guardado los datos de manera adecuada en ambos sistemas")
            else:
                self.mongoInstancia.guardar_json(nombre_json_temporal, diccionario)
        except:
            return False
        #dejar esto y luego hacer un try que returne un false o true para poder poner el codigo que sigue en la interfaz de las cosas // se hace esto porque para cargar las cosas del json temporal tengo que usar en el cargar lista de json temporal una forma de crear las cosas y eso lo hice hardcodeado en la practica pasada, ademas que tengo que cargar las cosas en su respectiva lista        
        # else:
        #     nuevojsonjeje = self.clienteInstancia.cargarListaJsonTemporal(jsontemporal)
        #     # print(jsonTemporalConvertido)
        #     # el jsontemporal tiene que pasar por el convertidor, porque si no me esta jodiendo la json
        #     se_guardo = self.mongoInstancia.guardarEnMongoParaTodos('Tienda', 'Clientes', nuevojsonjeje, 'clientes.json', 'clientesTemporales.json')
        #     if se_guardo == False:
        #         print("Pu;etas")
        #     else:
        #         print("Se han guardado los datos de manera adecuada en ambos sistemas")
        #         self.mongoInstancia.borrarJson("clientesTemporales.json")

    def cerrarConexion(self):
        self.mongoInstancia.cerrar_conexion()

    def borrar_json(self, json):
        self.mongoInstancia.borrar_json(json)