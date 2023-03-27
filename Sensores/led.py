import time
from gpiozero import LED
from Lista import lista
import datetime

class MyLed(lista.Lista):
    def __init__(self, pin):
        self.pin = pin
        self.led = LED(self.pin)
        super().__init__()

    def toggle(self):
        if self.led.is_lit:
            self.led.off()
            return 0
        else:
            self.led.on()
            return 1

    def estado(self):
        if self.led.is_lit:
            return 1
        else:
            return 0

    def diccionario(self, clave):
        estado = self.toggle()
        diccionario = {
            "clave": clave,
            "tipo":"LED",
            "descripcion":"Dispositivo semiconductor que emite luz",
            "pin":self.pin,
            "valor":estado,
            "tipo_dato":"booleano",
            "fecha":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return diccionario
    
    def cargar_lista_guardada_previamente(self):
        if super().cargar_lista_json("led.json") == False:
            return False
        else:
            nuevaLista = super().cargar_lista_json("led.json")
            for objetoIndividual in nuevaLista:
                diccionario  = {   
                    "clave" : objetoIndividual["clave"],
                    "tipo" : objetoIndividual["tipo"],
                    "descripcion" : objetoIndividual["descripcion"],
                    "pin" : objetoIndividual["pin"],
                    "valor" : objetoIndividual["valor"],
                    "tipo_dato" : objetoIndividual["tipo_dato"],
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
                valor = i["valor"]
                tipo_dato = i["tipo_dato"]
                fecha = i["fecha"]
                listanueva.append({
                    "clave":clave,
                    "tipo":tipo,
                    "descripcion":descripcion,
                    "pin":pin,
                    "valor":valor,
                    "tipo_dato":tipo_dato,
                    "fecha":fecha
                    })
            super().enviarDiccionarioYAlmacenamientoJson("led.json", listanueva)
            return listanueva
        except:
            return False
    

