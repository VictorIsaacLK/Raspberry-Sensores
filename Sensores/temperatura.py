import Adafruit_DHT
from Lista import lista
import datetime

class Temperatura(lista.Lista):
    def __init__(self, pin):
        self.pin = pin
        self.sensor = Adafruit_DHT.DHT11
        super().__init__()

    def leer_temperatura(self):
        humedad, temperatura = Adafruit_DHT.read_retry(self.sensor, self.pin)
        if humedad is not None and temperatura is not None:
            return humedad, temperatura
        else:
            print("Error al leer los datos")


    def diccionario(self, clave):
        humedad, temperatura = self.leer_temperatura()
        diccionario = {
            "clave": clave,
            "tipo":"Sensor DHT11",
            "descripcion":"Sensor que mide la humedad y temperatura",
            "pin":self.pin,
            "valor_humedad":humedad,
            "humedad_dato":"Porcentaje de Humedad",
            "valor_temperatura":temperatura,
            "temperatura_dato":"Grados Celcius",
            "humedad":"{} %".format(humedad),
            "temperatura":"{} °C".format(temperatura),
            "fecha":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return diccionario
    
    
    def cargar_lista_guardada_previamente(self):
        if super().cargar_lista_json("dht11.json") == False:
            return False
        else:
            nuevaLista = super().cargar_lista_json("dht11.json")
            for objetoIndividual in nuevaLista:
                diccionario  = {   
                    "clave" : objetoIndividual["clave"],
                    "tipo" : objetoIndividual["tipo"],
                    "descripcion" : objetoIndividual["descripcion"],
                    "pin": objetoIndividual["pin"],
                    "valor_humedad":objetoIndividual["valor_humedad"],
                    "humedad_dato":objetoIndividual["humedad_dato"],
                    "valor_temperatura":objetoIndividual["valor_temperatura"],
                    "temperatura_dato":objetoIndividual["temperatura_dato"],
                    "humedad":objetoIndividual["humedad"],
                    "temperatura":objetoIndividual["temperatura"],
                    "fecha" : objetoIndividual["fecha"],
                }
                self.add(diccionario)
    
    def cargar_lista_json_temporal(self, lista):
        try:
            listanueva = []
            for i in lista:
                clave = i["clave"]
                tipo = i["tipo"]
                descripcion = i["descripcion"]
                pin = i["pin"]
                valor_humedad = i["valor_humedad"]
                humedad_dato = i["humedad_dato"]
                valor_temperatura = i["valor_temperatura"]
                temperatura_dato = i["temperatura_dato"]
                humedad = i["humedad"]
                temperatura = i["temperatura"]
                fecha = i["fecha"]
                listanueva.append({
                    "clave":clave,
                    "tipo":tipo,
                    "descripcion":descripcion,
                    "pin":pin,
                    "valor_humedad":valor_humedad,
                    "humedad_dato":humedad_dato,
                    "valor_temperatura":valor_temperatura,
                    "temperatura_dato":temperatura_dato,
                    "humedad":humedad,
                    "temperatura":temperatura,
                    "fecha":fecha
                    })
            super().enviarDiccionarioYAlmacenamientoJson("dht11.json", listanueva)
            return listanueva
        except:
            return False
        
        
