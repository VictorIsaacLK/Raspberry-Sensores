import Adafruit_DHT
from Lista import lista
import datetime

class Humedad(lista.Lista):
    def __init__(self, pin):
        self.pin = pin
        self.sensor = Adafruit_DHT.DHT11
        super().__init__()

    #Lectura
    
    def leer_humedad(self):
        humedad, temperatura = Adafruit_DHT.read_retry(self.sensor, self.pin)
        if humedad is not None and temperatura is not None:
            return humedad
        else:
            print("Error al leer los datos")


    #Diccionario

    def diccionario_humedad(self, sensor):
        humedad = self.leer_humedad()
        diccionario = {
            "valor":humedad,
            "fecha":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "medida":"%",
            "sensor":sensor
        }
        return diccionario
    


    #Cargar listas

    def cargar_lista_guardada_previamente(self):
        if super().cargar_lista_json("humedad.json") == False:
            return False
        else:
            nuevaLista = super().cargar_lista_json("humedad.json")
            for objetoIndividual in nuevaLista:
                diccionario  = {
                    "valor" : objetoIndividual["valor"],
                    "fecha" : objetoIndividual["fecha"],
                    "medida": objetoIndividual["medida"],
                    "sensor": objetoIndividual["sensor"],
                }
                self.add(diccionario)
    
    def cargar_lista_json_temporal(self, lista):
        try:
            listanueva = []
            for i in lista:
                valor = i["valor"]
                fecha = i["fecha"]
                medida = i["medida"]
                sensor = i["sensor"]
                listanueva.append({
                    "valor":valor,
                    "fecha":fecha,
                    "medida":medida,
                    "sensor":sensor
                    })
            super().enviarDiccionarioYAlmacenamientoJson("humedad.json", listanueva)
            return listanueva
        except:
            return False
               
        
