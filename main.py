from InterfacesSensores import interfaz_compartida


def menu():
    interfaz_sensores = interfaz_compartida.InterfazCompartida()
    interfaz_sensores.menu_lectura()
    
menu()