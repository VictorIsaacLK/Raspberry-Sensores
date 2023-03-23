from Sensores import temperatura
from Mongo import mongo
import sys

class InterfazTemperatura():
    def __init__(self, temperaturaInstancia = temperatura.Temperatura(), mongoInstancia = mongo.MongoDB()):
        self.temperaturaInstancia = temperaturaInstancia
        self.mongoInstancia = mongoInstancia
        #cargar aqui todos los documentos guardados

    def seteo_temperatura(self, pin):
        pin = int(input("En que lugar existe el sensor de temperatura"))
        humedad, temperatura = self.temperaturaInstancia.leer_temperatura(pin)
        

