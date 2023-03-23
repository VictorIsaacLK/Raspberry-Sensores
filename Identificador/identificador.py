import random
import string


class Identificador():

    def crear_identificador(self):
        letras_numeros = string.ascii_letters + string.digits
        clave = ''.join(random.choice(letras_numeros) for i in range(5))
        return clave