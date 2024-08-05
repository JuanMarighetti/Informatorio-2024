import os
import platform
from cuentas import CuentaCorriente, CuentaAhorro, GestionCuentas

def limpiar_pantalla():
    ''' Limpiar la pantalla según el sistema operativo'''
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear') # Para Linux/Unix/MacOs

def mostrar_menu():
    print("========== Menú de Gestión de Cuentas Bancarias ==========")
    print('1. Agregar Cuenta Corriente')
    print('2. Agregar Cuenta de Ahorro')
    print('3. Buscar Cuenta por Número')
    print('4. Actualizar Saldo de Cuenta')
    print('5. Eliminar Cuenta por Número')
    print('6. Mostrar Todas las Cuentas')
    print('7. Salir')
    print('==========================================================')

def agregar_cuenta(gestion, tipo_cuenta):
    try:
        numero_cuenta = input('Ingrese número de cuenta: ')
        saldo = float(input('Ingrese saldo inicial: '))
        titular = input('Ingrese titular de la cuenta: ')
        fecha_ingreso = input('Ingrese fecha de ingreso (YYYY-MM-DD): ')

        if tipo_cuenta == '1':
            limite_descubierto = float(input('Ingrese límite descubierto: '))
            cuenta = CuentaCorriente(numero_cuenta, saldo, titular, fecha_ingreso, limite_descubierto)
        elif tipo_cuenta == '2':
            tasa_interes = float(input('Ingrese tasa de interés: '))
            cuenta = CuentaAhorro(numero_cuenta, saldo, titular, fecha_ingreso, tasa_interes)
        else:
            print('Opción inválida')
            return

        gestion.crear_cuenta(cuenta)
        input('Presione enter para continuar...')

    except ValueError as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f'Error inesperado: {e}')

def buscar_cuenta_por_numero(gestion):
    numero_cuenta = input('Ingrese el número de cuenta a buscar: ')
    cuenta = gestion.leer_cuenta(numero_cuenta)
    if cuenta:
        print(cuenta)
    input('Presione enter para continuar...')

def actualizar_saldo_cuenta(gestion):
    numero_cuenta = input('Ingrese el número de cuenta para actualizar saldo: ')
    saldo = float(input('Ingrese el nuevo saldo de la cuenta: '))
    gestion.actualizar_saldo(numero_cuenta, saldo)
    input('Presione enter para continuar...')

def eliminar_cuenta_por_numero(gestion):
    numero_cuenta = input('Ingrese el número de cuenta a eliminar: ')
    gestion.eliminar_cuenta(numero_cuenta)
    input('Presione enter para continuar...')

def mostrar_todas_las_cuentas(gestion):
    print('=============== Listado completo de las Cuentas ===============')
    for cuenta in gestion.leer_datos().values():
        if 'limite_descubierto' in cuenta:
            print(f"{cuenta['numero_cuenta']} - Titular: {cuenta['titular']} - Límite Descubierto: {cuenta['limite_descubierto']}")
        else:
            print(f"{cuenta['numero_cuenta']} - Titular: {cuenta['titular']} - Tasa de Interés: {cuenta['tasa_interes']}")
    print('===============================================================')
    input('Presione enter para continuar...')

if __name__ == "__main__":
    archivo_cuentas = 'cuentas_db.json'
    gestion = GestionCuentas(archivo_cuentas)

    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input('Seleccione una opción: ')

        if opcion == '1' or opcion == '2':
            agregar_cuenta(gestion, opcion)
        
        elif opcion == '3':
            buscar_cuenta_por_numero(gestion)

        elif opcion == '4':
            actualizar_saldo_cuenta(gestion)

        elif opcion == '5':
            eliminar_cuenta_por_numero(gestion)

        elif opcion == '6':
            mostrar_todas_las_cuentas(gestion)

        elif opcion == '7':
            print('Saliendo del programa...')
            break
        else:
            print('Opción no válida. Por favor, seleccione una opción válida (1-7)')
