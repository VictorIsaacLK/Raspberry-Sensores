#Libraries
import RPi.GPIO as GPIO
import time
from Lista import lista
import datetime

class Ultrasonico(lista.Lista):
    def __init__(self, trigger_pin, echo_pin):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
        #set GPIO Pins
        GPIO.setwarnings(False)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        #Instancia
        super().__init__()

    def limpiar_pin(self):
        GPIO.cleanup()

    def leer_distancia(self):
        GPIO.output(self.trigger_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin, False)
        time.sleep(0.00001)
        StartTime = time.time()
        StopTime = time.time()
        
        # Tiempo de inicio
        while GPIO.input(self.echo_pin) == 0:
            StartTime = time.time()

        # Tiempo de llegada
        while GPIO.input(self.echo_pin) == 1:
            StopTime = time.time()

        # Tiempo de diferencia entre la ida y llegada
        TimeElapsed = StopTime - StartTime

        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        return distance
    
    def diccionario(self, sensor):
        distancia = self.leer_distancia()
        diccionario = {
            "valor":distancia,
            "fecha":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "medida":"cm",
            "sensor":sensor
        }
        return diccionario
    
    def cargar_lista_guardada_previamente(self):
        if super().cargar_lista_json("ultrasonico.json") == False:
            return False
        else:
            nuevaLista = super().cargar_lista_json("ultrasonico.json")
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
            super().enviarDiccionarioYAlmacenamientoJson("ultrasonico.json", listanueva)
            return listanueva
        except:
            return False
    

