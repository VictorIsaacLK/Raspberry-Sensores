from Sensores import ultrasonico
from Mongo import interfaz_mongo
import sys

class InterfazUltrasonico():
    def __init__(self, mongoInstancia = interfaz_mongo.InterafazMongoDB()):
        self.mongoInstancia = mongoInstancia
        #cargar los documentos guardados

    def crearSensor(self):
        trigger_pin = int(input("Ingresa donde esta conectado el trigger pin: "))
        echo_pin = int(input("Ingresa donde esta conectado el echo pin: "))
        self.ultrasonicoInstancia = ultrasonico.Ultrasonico(trigger_pin, echo_pin)
        # ultrasonico.Ultrasonico(trigger_pin, echo_pin)
        self.guardar_datos()
        # return ultra
    
    def guardar_datos(self):
        info = self.ultrasonicoInstancia.diccionario()
        self.ultrasonicoInstancia.add(info)
        self.ultrasonicoInstancia.enviarDiccionarioYAlmacenamientoJson("ultrasonico.json", info)

    def leer_datos_guardados(self):
        self.ultrasonicoInstancia.cargar_lista_json("ultrasonico.json")
    
    def limpiar_pin(self):
        self.ultrasonicoInstancia.limpiar_pin()

    def returnar_diccionario(self):
        try:
            return self.ultrasonicoInstancia.leer_json()
        except:
            print("No se ha podido leer/NO EXISTEN los datos guardados")

    def menuInterfazUltrasonico(self):
        opcion = 0
        while opcion!= 9:
            print("---------------------------------------------------------------")
            print("[1] Ingresar Ultrasonico\n[2] Ver Datos\n[3]Limpiar pin\n[6] Mongo\n[9] Salida")
            print("---------------------------------------------------------------")
            try:
                opcion = int(input("Opcion: "))
            except ValueError:
                print("Opcion no valida")
            print("---------------------------------------------------------------")
            if opcion == 1:
                self.crearSensor()
                opcion = 0
            elif opcion == 2:
                self.leer_datos_guardados() #metodo que puede tiene que inicializarse
            elif opcion == 3:
                self.limpiar_pin()
            elif opcion == 9:
                self.mongoInstanciaTemporal()
                opcion = 0
    
    def mongoInstanciaTemporal(self):
        opcion = 0
        while opcion!= 9:
            self.mongoInstancia.MongoInterfaz()
            try:
                opcion = int(input("Opcion: "))
            except ValueError:
                print("Opcion no valida")
            if opcion == 1:
                url_conexion = input("Ingresa la url de conexion a mongoDB: ")
                self.mongoInstancia.conexion(url_conexion)
                opcion = 0
            elif opcion == 2:
                respuesta = self.mongoInstancia.guardarDatosEnMongo("ultrasonico.json", "temporal_ultrasonico.json", "Sensores", "DatoSensores", self.returnar_diccionario)

                if respuesta == False:
                    jsontemporal = self.ultrasonicoInstancia.cargar_lista_json("temporal_ultrasonico.json")
                    nuevojsonjeje = self.ultrasonicoInstancia.cargar_lista_json_temporal(jsontemporal)
                    se_guardo = self.mongoInstancia.guardarDatosEnMongo('Sensores', 'DatosSensores', nuevojsonjeje, 'ultrasonico,.json', 'clientesTemporales.json')
                    if se_guardo == False:
                        print("Pu;etas")
                    else:
                        print("Se han guardado los datos de manera adecuada en ambos sistemas")
                    self.mongoInstancia.borrar_json("temporal_ultrasonico.json")
            elif opcion == 3:
                self.mongoInstancia.cerrarConexion()

                

