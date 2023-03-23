from Sensores import ultrasonico
from Mongo import mongo
import sys

class InterfazUltrasonico():
    def __init__(self, ultrasonicoInstancia = ultrasonico.Ultrasonico(), mongoInstancia = mongo.MongoDB()):
        self.ultrasonicoInstancia = ultrasonicoInstancia
        self.mongoInstancia = mongoInstancia
        #cargar los documentos guardados

    def crearSensor(self):
        trigger_pin = int(input("Ingresa donde esta conectado el trigger pin: "))
        echo_pin = int(input("Ingresa donde esta conectado el echo pin: "))
        ultrasonico.Ultrasonico(trigger_pin, echo_pin)
        self.guardar_datos()
        # return ultra
    
    def guardar_datos(self):
        info = self.ultrasonicoInstancia.diccionario()
        self.ultrasonicoInstancia.add(info)
        self.ultrasonicoInstancia.enviarDiccionarioYAlmacenamientoJson("ultrasonico.json", info)

    def leer_datos_guardados(self):
        data = self.ultrasonicoInstancia.cargar_lista_json("ultrasonico.json")
        print(data)

    def menuInterfazUltrasonico(self):
        opcion = 0
        while opcion!= 9:
            print("---------------------------------------------------------------")
            print("[1] Ingresar Ultrasonico\n[2] Ver Datos\n[6] Mongo\n[9] Salida")
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
                self.leer_datos_guardados()

