import time
from gpiozero import LED
from Lista import lista

class MyLed(lista.Lista):
    def __init__(self, pin):
        self.pin = pin
        self.led = LED(self.pin)

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
