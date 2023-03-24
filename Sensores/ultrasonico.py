#Libraries
import RPi.GPIO as GPIO
import time
from Lista import lista
import datetime
from Identificador import identificador as identifier

class Ultrasonico(lista.Lista):
    def __init__(self, trigger_pin, echo_pin):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
        #set GPIO Pins
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        #Instancia del identificador
        self.identificador = identifier.Identificador()
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
        # save StartTime
        while GPIO.input(self.echo_pin) == 0:
            StartTime = time.time()

        # save time of arrival
        while GPIO.input(self.echo_pin) == 1:
            StopTime = time.time()

        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        return distance
    
    def diccionario(self):
        distancia = self.leer_distancia()
        diccionario = {
            "clave":self.identificador.crear_identificador(),
            "tipo":"Sensor de Distancia DHT11",
            "descripcion":"Sensor que mide la distancia",
            "trigger_pin":self.trigger_pin,
            "echo_pin":self.echo_pin,
            "valor":distancia,
            "fecha":datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        }
        return diccionario
    
    def cargar_lista_json_temporal(self, lista):
        listanueva = []
        for i in lista:
            clave = i["clave"]
            tipo = i["tipo"]
            descripcion = i["descripcion"]
            trigger_pin = i["trigger_pin"]
            echo_pin = i["echo_pin"]
            valor = i["valor"]
            fecha = i["fecha"]
            listanueva.append({
                "clave":clave,
                "tipo":tipo,
                "descripcion":descripcion,
                "trigger_pin":trigger_pin,
                "echo_pin":echo_pin,
                "valor":valor,
                "fecha":fecha
                })
        super().enviarDiccionarioYAlmacenamientoJson("ultrasonico.json", listanueva)
        return listanueva

