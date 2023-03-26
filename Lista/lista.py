from Json import json_conversion

class Lista(json_conversion.JsonConversion):
    def __init__(self):
        self.listita = []
        super().__init__()
    

    def add(self, item):
        self.listita.append(item)
    
    def return_list(self):
        return self.listita
    
    def leer_json(self, archivo_json):
        return super().cargar_lista_json(archivo_json)
    
    def enviarDiccionarioYAlmacenamientoJson(self, almacenamiento, diccionario):
        super().guardar_json(almacenamiento, diccionario)