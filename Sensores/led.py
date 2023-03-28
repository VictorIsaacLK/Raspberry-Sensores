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

    def diccionario(self, sensor):
        estado = self.toggle()
        diccionario = {
            "valor":estado,
            "fecha":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "medida":"bool",
            "sensor":sensor
        }
        return diccionario
    
    def cargar_lista_guardada_previamente(self):
        if super().cargar_lista_json("led.json") == False:
            return False
        else:
            nuevaLista = super().cargar_lista_json("led.json")
            for objetoIndividual in nuevaLista:
                diccionario  = {
                    "valor" : objetoIndividual["valor"],
                    "fecha" : objetoIndividual["fecha"],
                    "medida": objetoIndividual["medida"],
                    "sensor" : objetoIndividual["sensor"]
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
            super().enviarDiccionarioYAlmacenamientoJson("led.json", listanueva)
            return listanueva
        except:
            return False
    

