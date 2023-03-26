from InterfacesSensores import interfaz_compartida


def menu():
    opcion = 0
    interfaz_sensores = interfaz_compartida.InterfazCompartida()
    while opcion!= 9:
        print("---------------------------------------------------------------")
        print("Bienvenido al sistema, decida la opcion que necesite")
        print("[1] Entrar en el sistema\n[9] Salida")
        print("---------------------------------------------------------------")
        try:
            opcion = int(input("Opcion: "))
        except ValueError:
            print("Opcion no valida")
        if opcion == 1:
            print("Recuerda! Actualmente solo existen 3 sensores:\nSensor Ultrasonico\nSensor de Temperatura y Humedad\nLED")
            # interfaz_ultrasonico_instancia.menuInterfazUltrasonico()
            interfaz_sensores.menu_introductorio()
            opcion = 0


menu()