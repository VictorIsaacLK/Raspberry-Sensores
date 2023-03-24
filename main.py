from InterfacesSensores import interfaz_ultrasonico


def menu():
    opcion = 0
    interfaz_ultrasonico_instancia = interfaz_ultrasonico.InterfazUltrasonico()
    while opcion!= 9:
        print("---------------------------------------------------------------")
        print("Bienvenido al sistema, decida la opcion que necesite")
        print("[1] Ultrasonico\n[2] Humedad y Temperatura\n[3] Led\n[9] Salida")
        print("---------------------------------------------------------------")
        try:
            opcion = int(input("Opcion: "))
        except ValueError:
            print("Opcion no valida")
        if opcion == 1:
            interfaz_ultrasonico_instancia.menuInterfazUltrasonico()
            opcion = 0


menu()