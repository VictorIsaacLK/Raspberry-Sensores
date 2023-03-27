from Sensores import ultrasonico
from Mongo import interfaz_mongo
import time
from Identificador import identificador as identifier
import sys
import select
from Sensores import temperatura

class InterfazCompartida():
    def __init__(self, mongoInstancia = interfaz_mongo.InterafazMongoDB()):
        self.mongoInstancia = mongoInstancia
        self.identificador = identifier.Identificador()
        #cargar los documentos guardados


    def detente(self, segundos):
        time.sleep(segundos)
    
    def crear_sensores(self):
        print("A continuacion, agregaras como estan acomodados los pines de los sensores")
        
        #Seccion sensor ultrasonico
        print("Seccion sensor ultrasonico")
        trigger_pin = int(input("Ingresa donde esta conectado el trigger pin: "))
        echo_pin = int(input("Ingresa donde esta conectado el echo pin: "))
        self.ultrasonicoInstancia = ultrasonico.Ultrasonico(trigger_pin, echo_pin)
        self.ultrasonicoInstancia.cargar_lista_guardada_previamente()

        #Seccion sensor dht11
        print("Seccion sensor dht11")
        pin_dht11 = int(input("Ingresa donde esta conectado el pin: "))
        self.dht11Instancia = temperatura.Temperatura(pin_dht11)
        self.dht11Instancia.cargar_lista_guardada_previamente()


    def leer_y_guardar_datos(self):
        opcion = 0
        clave = self.identificador.crear_identificador()
        while opcion!= 9:

            self.detente(2)
            #Seccion sensor ultrasonico

            info = self.ultrasonicoInstancia.diccionario(clave)
            self.ultrasonicoInstancia.add(info)
            listaUltrasonica = self.ultrasonicoInstancia.return_list()
            self.ultrasonicoInstancia.enviarDiccionarioYAlmacenamientoJson("ultrasonico.json", listaUltrasonica)
            print(info)

            #Seccion sensor dht11
            info_dht11 = self.dht11Instancia.diccionario(clave)
            self.dht11Instancia.add(info_dht11)
            listaDht11 = self.dht11Instancia.return_list()
            self.dht11Instancia.enviarDiccionarioYAlmacenamientoJson("dht11.json", listaDht11)
            print(info_dht11)

            ready, _, _ = select.select([sys.stdin], [], [], 1.0)
            if ready:
                key = sys.stdin.read(1)
                if key == '9':
                    break

    def leer_datos_guardados(self):
        
        #Aqui van a estar todos juntos
        datosUltra = self.ultrasonicoInstancia.cargar_lista_json("ultrasonico.json")
        datosDht11 = self.dht11Instancia.cargar_lista_json("dht11.json")
        if datosUltra == datosDht11 == False:
            print("No existen datos actualmente")
            return False
        else:
            print(datosUltra)
            print("----------------\n\n\n\n\n\n\n----------\n\n\n\n\n--------------------")
            print(datosDht11)
    

    #creo que tampoco ha sido usado
    def limpiar_pin(self):
        try:
            self.ultrasonicoInstancia.limpiar_pin()
        except:
            print("No existe actualmente")
            return False

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
    

    def menu_introductorio(self):
        opcion = 0
        while opcion!= 9:
            print("---------------------------------------------------------------")
            print("[1] Ingresar Sensores\n[9] Salida")
            print("---------------------------------------------------------------")
            try:
                opcion = int(input("Opcion: "))
            except ValueError:
                print("Opcion no valida")
            print("---------------------------------------------------------------")
            if opcion == 1:
                self.crear_sensores()
                opcion = 0
                self.menu_lectura()

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

    #creo que no ha sido usado
    def menu_interfaz_sensores(self):
        opcion = 0
        while opcion != 0:
            print("---------------------------------------------------------------")
            print("[1] Ultrasonico\n[2] Humedad y Temperatura\n[3] LED\n[9] Salida")
            print("---------------------------------------------------------------")

    #tampoco ha sido usado
    def menu_ultrasonico(self):
        opcion = 0
        while opcion!= 9:
            print("---------------------------------------------------------------")
            print("\n[1] Ver Datos\n[2]Limpiar pin\n[6] Mongo\n[9] Salida")
            print("---------------------------------------------------------------")
            try:
                opcion = int(input("Opcion: "))
            except ValueError:
                print("Opcion no valida")
            print("---------------------------------------------------------------")
            if opcion == 1:
                self.leer_datos_guardados() #metodo que puede tiene que inicializarse
                opcion = 0
            elif opcion == 3:
                self.limpiar_pin()
                opcion = 0
            elif opcion == 6:
                self.mongoInstanciaTemporal()
                opcion = 0
            elif opcion == 9:
                self.mongoInstanciaTemporal()
                opcion = 0
    
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