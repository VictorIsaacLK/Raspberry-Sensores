import Adafruit_DHT

# Configuración del tipo de sensor y del pin GPIO
sensor = Adafruit_DHT.DHT11
pin = 20

# Lectura de los datos del sensor
humedad, temperatura = Adafruit_DHT.read_retry(sensor, pin)

# Comprobación si la lectura ha sido correcta
if humedad is not None and temperatura is not None:
    print('Temperatura={0:0.1f}*C  Humedad={1:0.1f}%'.format(temperatura, humedad))
else:
    print('Error al leer los datos del sensor')



