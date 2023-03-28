from Sensores import ultrasonico
from Mongo import interfaz_mongo
import time
from Identificador import identificador as identifier
import sys
import select
from Sensores import temperatura
from Sensores import led
from termcolor import colored
from Sensores import sensor

class InterfazCompartida():
    def __init__(self, mongoInstancia = interfaz_mongo.InterafazMongoDB(), sensorIntancia = sensor.Sensor()):
        self.mongoInstancia = mongoInstancia
        self.sensorIntancia = sensorIntancia
        self.identificador = identifier.Identificador()
        #cargar los documentos guardados

    def detente(self, segundos):
        time.sleep(segundos)
    
    def crear_sensores(self):
        
        clave = self.identificador.crear_identificador()

        #Seccion sensor ultrasonico
        print("Seccion sensor ultrasonico")
        trigger_pin = int(input("Ingresa donde esta conectado el trigger pin: "))
        echo_pin = int(input("Ingresa donde esta conectado el echo pin: "))
        self.ultrasonicoInstancia = ultrasonico.Ultrasonico(trigger_pin, echo_pin)
        sensor_info_ultra = self.sensorIntancia.diccionario_sensor(clave, "Ultrasonico HC-SR04", "Mide la distancia", [trigger_pin, echo_pin])
        self.ultrasonicoInstancia.cargar_lista_guardada_previamente()

        #Seccion sensor dht11
        print("Seccion sensor dht11")
        pin_dht11 = int(input("Ingresa donde esta conectado el pin: "))
        self.dht11Instancia = temperatura.Temperatura(pin_dht11)
        sensor_info_dht11 = self.sensorIntancia.diccionario_sensor(clave, "Sensor dht11", "Mide la temperatura y distancia", [pin_dht11])
        self.dht11Instancia.cargar_lista_guardada_previamente("humedad.json", "temperatura.json")

        #Secccion LED
        print("Seccion LED")
        pin_led = int(input("Ingresa donde esta conectado el pin: "))
        self.ledInstancia = led.MyLed(pin_led)
        info_led = self.sensorIntancia.diccionario_sensor(clave, "LED", "Diodo Emisor de Luz", [pin_led])
        self.ledInstancia.cargar_lista_guardada_previamente()

        return sensor_info_ultra, sensor_info_dht11, info_led


    def leer_y_guardar_datos(self):
        sensor_info_ultra, sensor_info_dht11, info_led = self.crear_sensores()
        opcion = 0
        while opcion!= 9:

            self.detente(2)
            #Seccion sensor ultrasonico

            info = self.ultrasonicoInstancia.diccionario(sensor_info_ultra)
            self.ultrasonicoInstancia.add(info)
            listaUltrasonica = self.ultrasonicoInstancia.return_list()
            self.ultrasonicoInstancia.enviarDiccionarioYAlmacenamientoJson("ultrasonico.json", listaUltrasonica)
            print(info)

            #Seccion sensor dht11
            info_dht11 = self.dht11Instancia.diccionario(sensor_info_dht11)
            self.dht11Instancia.add(info_dht11)
            listaDht11 = self.dht11Instancia.return_list()
            self.dht11Instancia.enviarDiccionarioYAlmacenamientoJson("dht11.json", listaDht11)
            print(info_dht11)

            #Seccion LED
            info_led = self.ledInstancia.diccionario(info_led)
            self.ledInstancia.add(info_led)
            listaLed = self.ledInstancia.return_list()
            self.ledInstancia.enviarDiccionarioYAlmacenamientoJson("led.json", listaLed)
            print(info_led)

            ready, _, _ = select.select([sys.stdin], [], [], 1.0)
            if ready:
                key = sys.stdin.read(1)
                if key == '9':
                    break

    def leer_datos_guardados(self):
        
        #Aqui van a estar todos juntos
        datosUltra = self.ultrasonicoInstancia.cargar_lista_json("ultrasonico.json")
        datosDht11 = self.dht11Instancia.cargar_lista_json("dht11.json")
        datosLed = self.ledInstancia.cargar_lista_json("led.json")
        if datosUltra == datosDht11 == datosLed == False:
            print("No existen datos actualmente")
            return False
        else:
            self.mostrar_info_temperatura(datosDht11)
            print("-----------\n\n\----------")
            self.mostrar_info_ultrasonico(datosUltra)
            print("-----------\n\n----------")
            self.mostrar_info_led(datosLed)


    def returnar_diccionario_ultrasonico(self):
        #informacion =  self.ultrasonicoInstancia.leer_json("ultrasonico.json")
        informacion = self.ultrasonicoInstancia.return_list() #prueba a ver si se puede con la lista
        if informacion == False:
            print("No existen datos actualmente")
            return False
        else:
            return informacion
        
    
    def returnar_diccionario_dht11(self):
        informacion = self.dht11Instancia.return_list()
        if informacion == False:
            print("No existen datos actualmente")
            return False
        else:
            return informacion
        
    def returnar_diccionario_led(self):
        informacion = self.ledInstancia.return_list()
        if informacion == False:
            print("No existen datos actualmente")
            return False
        else:
            return informacion

    def menu_lectura(self):
        opcion = 0
        while opcion!= 9:
            print("---------------------------------------------------------------")
            print("[1] Activar los sensores\n[2] Ver informacion\n[3] Mongo\n[9] Salida")
            print("---------------------------------------------------------------")
            try:
                opcion = int(input("Opcion: "))
            except ValueError:
                print("Opcion no valida")
            print("---------------------------------------------------------------")
            if opcion == 1:
                print("Para terminar esta funcion, precione 9")
                self.detente(2)
                self.leer_y_guardar_datos()
                opcion = 0
            elif opcion == 2:
                self.leer_datos_guardados()
                opcion = 0
            elif opcion == 3:
                self.mongoInstanciaTemporal()
                opcion = 0
        #Al salir, se limpiaran los pines para que podamos usarlos despues
        self.ultrasonicoInstancia.limpiar_pin()

    
    def mongoInstanciaTemporal(self):
        opcion = 0
        while opcion!= 9:
            self.mongoInstancia.MongoInterfaz()
            try:
                opcion = int(input("Opcion: "))
            except ValueError:
                print("Opcion no valida")
            if opcion == 1:
                url_conexion = input("Ingresa la url de conexion a mongoDB: ")
                self.mongoInstancia.conexion(url_conexion)
                opcion = 0
            elif opcion == 2:
                #Aqui empieza lo bueno
                self.ultrasonico_mongo()
                self.dht11_mongo()
                self.led_mongo()
                opcion = 0
            elif opcion == 3:
                self.mongoInstancia.cerrarConexion()
    
    def ultrasonico_mongo(self):
        jsontemporal = self.mongoInstancia.mongoInstancia.cargar_lista_json("temporal_ultrasonico.json")
        if jsontemporal == False:
            print("No existe ningun archivo temporal actualmente")
            se_guardo = self.mongoInstancia.mongoInstancia.guardar_en_mongo('Sensores', 'DatoSensorUltrasonico', self.returnar_diccionario_ultrasonico(), 'ultrasonico.json', 'temporal_ultrasonico.json') #se llama gaurdar en mongo en la nueva
            if se_guardo == False:
                print("No existe conexion con la base de datos, se han guardado los datos de manera temporal")
                # De aqui en adelante si exite la conexion, al menos en este if, es cuando no existe ar temporal, pero si conexion            
            else:
                print("Se han guardado los datos de manera adecuada en ambos sistemas")
        else:
            nuevojsonjeje = self.ultrasonicoInstancia.cargar_lista_json_temporal(jsontemporal)
            # print(jsonTemporalConvertido)
            # el jsontemporal tiene que pasar por el convertidor, porque si no me esta jodiendo la json
            se_guardo = self.mongoInstancia.mongoInstancia.guardar_en_mongo('Sensores', 'DatoSensorUltrasonico', nuevojsonjeje, 'ultrasonico.json', 'temporal_ultrasonico.json')
            if se_guardo == False:
                print("Pu;etas")
            else:
                print("Se han guardado los datos de manera adecuada en ambos sistemas")
                self.mongoInstancia.mongoInstancia.borrar_json("temporal_ultrasonico.json")




        #Se usa en el metodo que no sirve de mongo, despues lo arreglo

        # respuesta = self.mongoInstancia.guardarDatosEnMongo("ultrasonico.json", "temporal_ultrasonico.json", "Sensores", "DatoSensores", self.returnar_diccionario_ultrasonico())
        # if respuesta == False:
        #     jsontemporal = self.ultrasonicoInstancia.cargar_lista_json("temporal_ultrasonico.json")
            
        #     #si json temporal no existe, entonces se crea
        #     if jsontemporal == False:
        #         print("No existe conexion, se creara un archivo temporal para cuando exista conexion")
        #     else:
        #         nuevojsonjeje = self.ultrasonicoInstancia.cargar_lista_json_temporal(jsontemporal)
        #         se_guardo = self.mongoInstancia.guardarDatosEnMongo('Sensores', 'DatoSensores', nuevojsonjeje, 'ultrasonico.json', 'temporal_ultrasonico.json')
        #         if se_guardo == False:
        #             print("Pu;etas")
        #         else:
        #             print("Se han guardado los datos de manera adecuada en ambos sistemas")
        #             self.mongoInstancia.borrar_json("temporal_ultrasonico.json")


    def dht11_mongo(self):
        jsontemporal = self.mongoInstancia.mongoInstancia.cargar_lista_json("temporal_dht11.json")
        if jsontemporal == False:
            print("No existe ningun archivo temporal actualmente")
            se_guardo = self.mongoInstancia.mongoInstancia.guardar_en_mongo('Sensores', 'DatoSensorDHT11', self.returnar_diccionario_dht11(), 'dht11.json', 'temporal_dht11.json')
            if se_guardo == False:
                print("No existe conexion con la base de datos, se han guardado los datos de manera temporal")   
            else:
                print("Se han guardado los datos de manera adecuada en ambos sistemas")
        else:
            nuevojsonjeje = self.dht11Instancia.cargar_lista_json_temporal(jsontemporal)
            # print(jsonTemporalConvertido)
            # el jsontemporal tiene que pasar por el convertidor, porque si no me esta jodiendo la json
            se_guardo = self.mongoInstancia.mongoInstancia.guardar_en_mongo('Sensores', 'DatoSensorDHT11', nuevojsonjeje, 'dht11.json', 'temporal_dht11.json')
            if se_guardo == False:
                print("Pu;etas")
            else:
                print("Se han guardado los datos de manera adecuada en ambos sistemas")
                self.mongoInstancia.mongoInstancia.borrar_json("temporal_dht11.json")
    
    
    def led_mongo(self):
        jsontemporal = self.mongoInstancia.mongoInstancia.cargar_lista_json("temporal_led.json")
        if jsontemporal == False:
            print("No existe ningun archivo temporal actualmente")
            se_guardo = self.mongoInstancia.mongoInstancia.guardar_en_mongo('Sensores', 'DatoSensorLED', self.returnar_diccionario_led(), 'led.json', 'temporal_led.json')
            if se_guardo == False:
                print("No existe conexion con la base de datos, se han guardado los datos de manera temporal")   
            else:
                print("Se han guardado los datos de manera adecuada en ambos sistemas")
        else:
            nuevojsonjeje = self.ledInstancia.cargar_lista_json_temporal(jsontemporal)
            # print(jsonTemporalConvertido)
            # el jsontemporal tiene que pasar por el convertidor, porque si no me esta jodiendo la json
            se_guardo = self.mongoInstancia.mongoInstancia.guardar_en_mongo('Sensores', 'DatoSensorLED', nuevojsonjeje, 'led.json', 'temporal_led.json')
            if se_guardo == False:
                print("Pu;etas")
            else:
                print("Se han guardado los datos de manera adecuada en ambos sistemas")
                self.mongoInstancia.mongoInstancia.borrar_json("temporal_led.json")

    
    def mostrar_info_temperatura(self, diccionario):
        try:
            diccionarioDHT11 = diccionario
            clave_max_len = max([len(str(c['clave'])) for c in diccionarioDHT11])
            tipo_max_len = max([len(c['tipo']) for c in diccionarioDHT11])
            descripcion_max_len = max([len(c['descripcion']) for c in diccionarioDHT11])
            pin_max_len = max([len(str(c['pin'])) for c in diccionarioDHT11])
            humedad_max_len = max([len(str(c['valor_humedad'])) for c in diccionarioDHT11])
            humedad_dato_max_len = max([len(c['humedad_dato']) for c in diccionarioDHT11])
            temperatura_max_len = max([len(str(c['valor_temperatura'])) for c in diccionarioDHT11])
            temperatura_dato_max_len = max([len(c['temperatura_dato']) for c in diccionarioDHT11])
            fecha_max_len = max([len(c['fecha']) for c in diccionarioDHT11])
            
            print('-' * (clave_max_len + tipo_max_len + descripcion_max_len + pin_max_len + humedad_max_len + humedad_dato_max_len + temperatura_max_len + temperatura_dato_max_len + fecha_max_len + 18))
            print(colored('| {0:^{1}} | {2:^{3}} | {4:^{5}} | {6:^{7}} | {8:^{9}} | {10:^{11}} | {12:^{13}} | {14:^{15}} | {16:^{17}} |'.format('Clave', clave_max_len, 'Tipo', tipo_max_len, 'Descripcion', descripcion_max_len, 'Pin', pin_max_len, 'Humedad', humedad_max_len, 'Humedad Dato', humedad_dato_max_len, 'Temperatura', temperatura_max_len, 'Temperatura Dato', temperatura_dato_max_len, 'Fecha', fecha_max_len), "yellow"))
            print('-' * (clave_max_len + tipo_max_len + descripcion_max_len + pin_max_len + humedad_max_len + humedad_dato_max_len + temperatura_max_len + temperatura_dato_max_len + fecha_max_len + 18))
            
            for cliente in diccionarioDHT11:
                print('| {0:^{1}} | {2:^{3}} | {4:^{5}} | {6:^{7}} | {8:^{9}} | {10:^{11}} | {12:^{13}} | {14:^{15}} | {16:^{17}} |'.format(str(cliente['clave']), clave_max_len, cliente['tipo'], tipo_max_len, cliente['descripcion'], descripcion_max_len, str(cliente['pin']), pin_max_len, str(cliente['valor_humedad']), humedad_max_len, cliente['humedad_dato'], humedad_dato_max_len, str(cliente['valor_temperatura']), temperatura_max_len, cliente['temperatura_dato'], temperatura_dato_max_len, cliente['fecha'], fecha_max_len))
                print('-' * (clave_max_len + tipo_max_len + descripcion_max_len + pin_max_len + humedad_max_len + humedad_dato_max_len + temperatura_max_len + temperatura_dato_max_len + fecha_max_len + 18))
        except:
            print("No hay clientes registrados")

    def mostrar_info_ultrasonico(self, diccionario):
        try:
            diccionarioUltrasonico = diccionario
            clave_max_len = max([len(obj['clave']) for obj in diccionarioUltrasonico])
            tipo_max_len = max([len(obj['tipo']) for obj in diccionarioUltrasonico])
            descripcion_max_len = max([len(obj['descripcion']) for obj in diccionarioUltrasonico])
            valor_max_len = max([len(str(obj['valor'])) for obj in diccionarioUltrasonico])
            tipo_dato_max_len = max([len(obj['tipo_dato']) for obj in diccionarioUltrasonico])
            distancia_max_len = max([len(str(obj['Distancia'])) for obj in diccionarioUltrasonico])
            fecha_max_len = max([len(obj['fecha']) for obj in diccionarioUltrasonico])

            print('-' * (clave_max_len + tipo_max_len + descripcion_max_len + valor_max_len + tipo_dato_max_len + distancia_max_len + fecha_max_len + 17))
            print(colored('| {0:^{1}} | {2:^{3}} | {4:^{5}} | {6:^{7}} | {8:^{9}} | {10:^{11}} | {12:^{13}} |'.format('Clave', clave_max_len, 'Tipo', tipo_max_len, 'Descripcion', descripcion_max_len, 'Valor', valor_max_len, 'Tipo de Dato', tipo_dato_max_len, 'Distancia', distancia_max_len, 'Fecha', fecha_max_len), "yellow"))
            print('-' * (clave_max_len + tipo_max_len + descripcion_max_len + valor_max_len + tipo_dato_max_len + distancia_max_len + fecha_max_len + 17))

            for objeto in diccionarioUltrasonico:
                print('| {0:^{1}} | {2:^{3}} | {4:^{5}} | {6:^{7}} | {8:^{9}} | {10:^{11}} | {12:^{13}} |'.format(objeto['clave'], clave_max_len, objeto['tipo'], tipo_max_len, objeto['descripcion'], descripcion_max_len, objeto['valor'], valor_max_len, objeto['tipo_dato'], tipo_dato_max_len, objeto['Distancia'], distancia_max_len, objeto['fecha'], fecha_max_len))
                print('-' * (clave_max_len + tipo_max_len + descripcion_max_len + valor_max_len + tipo_dato_max_len + distancia_max_len + fecha_max_len + 17))
        except:
            print("No hay objetos registrados")

    def mostrar_info_led(self, objetos):
        try:
            clave_max_len = max([len(obj['clave']) for obj in objetos])
            tipo_max_len = max([len(obj['tipo']) for obj in objetos])
            descripcion_max_len = max([len(obj['descripcion']) for obj in objetos])
            pin_max_len = max([len(str(obj['pin'])) for obj in objetos])
            valor_max_len = max([len(str(obj['valor'])) for obj in objetos])
            tipo_dato_max_len = max([len(obj['tipo_dato']) for obj in objetos])
            fecha_max_len = max([len(obj['fecha']) for obj in objetos])

            print('-' * (clave_max_len + tipo_max_len + descripcion_max_len + pin_max_len + valor_max_len + tipo_dato_max_len + fecha_max_len + 14))
            print(colored('| {0:^{1}} | {2:^{3}} | {4:^{5}} | {6:^{7}} | {8:^{9}} | {10:^{11}} | {12:^{13}} |'.format('Clave', clave_max_len, 'Tipo', tipo_max_len, 'Descripción', descripcion_max_len, 'Pin', pin_max_len, 'Valor', valor_max_len, 'Tipo Dato', tipo_dato_max_len, 'Fecha', fecha_max_len), "yellow"))
            print('-' * (clave_max_len + tipo_max_len + descripcion_max_len + pin_max_len + valor_max_len + tipo_dato_max_len + fecha_max_len + 14))

            for obj in objetos:
                print('| {0:^{1}} | {2:^{3}} | {4:^{5}} | {6:^{7}} | {8:^{9}} | {10:^{11}} | {12:^{13}} |'.format(obj['clave'], clave_max_len, obj['tipo'], tipo_max_len, obj['descripcion'], descripcion_max_len, obj['pin'], pin_max_len, obj['valor'], valor_max_len, obj['tipo_dato'], tipo_dato_max_len, obj['fecha'], fecha_max_len))
                print('-' * (clave_max_len + tipo_max_len + descripcion_max_len + pin_max_len + valor_max_len + tipo_dato_max_len + fecha_max_len + 14))
        except:
            print("No hay objetos registrados")
