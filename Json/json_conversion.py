import json
import os

class JsonConversion():   
    #----------------------------METODOS--------------------------------#
    
    def guardar_json(self, almacenamiento, diccionario):
        with open(almacenamiento, 'w') as archivo:
            json.dump(diccionario, archivo, indent=4)
            
    def cargar_lista_json(self, almacenamiento):
        try:
            with open(almacenamiento, 'r') as archivo:
                data = json.load(archivo)
            return data
        except:
            return False
    
    def limpiar_todos_archivos(self):
        for documento in os.listdir():
            if documento.endswith(".json"):
                os.remove(documento)

    def limpiar_archivo(self, almacenamiento):
        os.remove(almacenamiento)
    #--------------------------------------------------------------------#   