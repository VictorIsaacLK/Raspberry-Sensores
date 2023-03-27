from Lista import lista
import datetime


class Sensor(lista.Lista):
    def __init__(self):
        super().__init__()
    

    def diccionario_sensor(self, clave, tipo, descripcion, pines):
        diccionario = {
            "clave": clave,
            "tipo":tipo,
            "descripcion":descripcion,
            "pines":pines
        }
        return diccionario
    
    
    def cargar_lista_guardada_previamente(self):
        if super().cargar_lista_json("sensores.json") == False:
            return False
        else:
            nuevaLista = super().cargar_lista_json("sensores.json")
            for objetoIndividual in nuevaLista:
                diccionario  = {   
                    "clave" : objetoIndividual["clave"],
                    "tipo" : objetoIndividual["tipo"],
                    "descripcion" : objetoIndividual["descripcion"],
                    "pines": objetoIndividual["pines"]
                }
                self.add(diccionario)
    
    def cargar_lista_json_temporal(self, lista):
        try:
            listanueva = []
            for i in lista:
                clave = i["clave"]
                tipo = i["tipo"]
                descripcion = i["descripcion"]
                pines = i["pines"]
                listanueva.append({
                    "clave":clave,
                    "tipo":tipo,
                    "descripcion":descripcion,
                    "pin":pines,
                    })
            super().enviarDiccionarioYAlmacenamientoJson("sensores.json", listanueva)
            return listanueva
        except:
            return False
