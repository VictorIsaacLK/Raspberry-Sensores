import Adafruit_DHT
from Lista import lista
import datetime

class Temperatura(lista.Lista):
    def __init__(self, pin):
        self.pin = pin
        self.sensor = Adafruit_DHT.DHT11
        super().__init__()

    #Lectura
    def leer_temperatura(self):
        humedad, temperatura = Adafruit_DHT.read_retry(self.sensor, self.pin)
        if humedad is not None and temperatura is not None:
            return temperatura
        else:
            print("Error al leer los datos")
    
    def leer_humedad(self):
        humedad, temperatura = Adafruit_DHT.read_retry(self.sensor, self.pin)
        if humedad is not None and temperatura is not None:
            return humedad
        else:
            print("Error al leer los datos")


    #Diccionario

    def diccionario_temperatura(self, sensor):
        temperatura = self.leer_temperatura()
        diccionario = {
            "valor":temperatura,
            "fecha":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "sensor":sensor
        }
        return diccionario
    
    def diccionario_humedad(self, sensor):
        humedad = self.leer_humedad()
        diccionario = {
            "valor":humedad,
            "fecha":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "sensor":sensor
        }
        return diccionario
    


    #Cargar listas

    def cargar_lista_guardada_previamente(self, lista_jsons):
        for eachJson in lista_jsons:
            if super().cargar_lista_json(eachJson) == False:
                return False
            else:
                nuevaLista = super().cargar_lista_json(eachJson)
                for objetoIndividual in nuevaLista:
                    diccionario  = {
                        "valor":objetoIndividual["valor"],
                        "fecha" : objetoIndividual["fecha"],
                        "sensor":objetoIndividual["sensor"]
                    }
                    self.add(diccionario)
    
    def cargar_lista_json_temporal(self, lista, listaJson):
        try:
            for EachJson in listaJson:
                listanueva = []
                for i in lista:
                    valor = i["valor"]
                    fecha = i["fecha"]
                    sensor = i["sensor"]
                    listanueva.append({
                        "valor":valor,
                        "fecha":fecha,
                        "sensor":sensor
                        })
                super().enviarDiccionarioYAlmacenamientoJson(EachJson, listanueva)
                return listanueva
        except:
            return False
               
        
