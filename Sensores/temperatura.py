import Adafruit_DHT
from Lista import lista

class Temperatura(lista.Lista):
    def __init__(self):
        self.sensor = Adafruit_DHT.DHT11

    def leer_temperatura(self, pin):
        humedad, temperatura = Adafruit_DHT.read_retry(self.sensor, pin)
        if humedad is not None and temperatura is not None:
            return humedad, temperatura
        else:
            print("Error al leer los datos")