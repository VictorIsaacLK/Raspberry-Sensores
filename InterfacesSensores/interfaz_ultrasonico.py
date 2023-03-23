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

    
