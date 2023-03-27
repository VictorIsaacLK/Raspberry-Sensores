from Lista import lista
import datetime


class Sensor(lista.Lista):
    def __init__(self):
        super().__init__()
    

    def diccionario_sensor(self, info_sensor):
        diccionario = {
            "clave": info_sensor['clave'],
            "tipo":info_sensor['tipo'],
            "descripcion":info_sensor['descripcion'],
            "dato":info_sensor['dato']
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
