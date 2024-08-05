import json
from datetime import datetime

class CuentaBancaria:
    def __init__(self, numero_cuenta, saldo, titular, fecha_ingreso):
        self.__numero_cuenta = numero_cuenta
        self.__saldo = self.validar_saldo(saldo)
        self.__titular = titular
        self.__fecha_ingreso = self.validar_fecha(fecha_ingreso)

    @property
    def numero_cuenta(self):
        return self.__numero_cuenta

    @property
    def saldo(self):
        return self.__saldo

    @saldo.setter
    def saldo(self, nuevo_saldo):
        self.__saldo = self.validar_saldo(nuevo_saldo)

    @property
    def titular(self):
        return self.__titular

    @property
    def fecha_ingreso(self):
        return self.__fecha_ingreso

    def validar_saldo(self, saldo):
        try:
            saldo_num = float(saldo)
            if saldo_num < 0:
                raise ValueError("El saldo debe ser positivo.")
            return saldo_num
        except ValueError:
            raise ValueError("El saldo debe ser un número válido.")

    def validar_fecha(self, fecha):
        try:
            return datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            raise ValueError("La fecha debe estar en formato YYYY-MM-DD.")

    def to_dict(self):
        return {
            "numero_cuenta": self.numero_cuenta,
            "saldo": self.saldo,
            "titular": self.titular,
            "fecha_ingreso": self.fecha_ingreso.strftime("%Y-%m-%d")
        }

    def __str__(self):
        return f"{self.numero_cuenta} - Titular: {self.titular}"

class CuentaCorriente(CuentaBancaria):
    def __init__(self, numero_cuenta, saldo, titular, fecha_ingreso, limite_descubierto):
        super().__init__(numero_cuenta, saldo, titular, fecha_ingreso)
        self.__limite_descubierto = limite_descubierto

    @property
    def limite_descubierto(self):
        return self.__limite_descubierto

    def to_dict(self):
        data = super().to_dict()
        data["limite_descubierto"] = self.limite_descubierto
        return data

    def __str__(self):
        return f"{super().__str__()} - Límite Descubierto: {self.limite_descubierto}"

class CuentaAhorro(CuentaBancaria):
    def __init__(self, numero_cuenta, saldo, titular, fecha_ingreso, tasa_interes):
        super().__init__(numero_cuenta, saldo, titular, fecha_ingreso)
        self.__tasa_interes = tasa_interes

    @property
    def tasa_interes(self):
        return self.__tasa_interes

    def to_dict(self):
        data = super().to_dict()
        data["tasa_interes"] = self.tasa_interes
        return data

    def __str__(self):
        return f"{super().__str__()} - Tasa de Interés: {self.tasa_interes}"

class GestionCuentas:
    def __init__(self, archivo):
        self.archivo = archivo

    def leer_datos(self):
        try:
            with open(self.archivo, 'r') as file:
                datos = json.load(file)
        except FileNotFoundError:
            return {}
        except Exception as error:
            raise Exception(f'Error al leer datos del archivo: {error}')
        else:
            return datos

    def guardar_datos(self, datos):
        try:
            with open(self.archivo, 'w') as file:
                json.dump(datos, file, indent=4)
        except IOError as error:
            print(f'Error al intentar guardar los datos en {self.archivo}: {error}')
        except Exception as error:
            print(f'Error inesperado: {error}')

    def crear_cuenta(self, cuenta):
        try:
            datos = self.leer_datos()
            numero_cuenta = cuenta.numero_cuenta
            if not str(numero_cuenta) in datos.keys():
                datos[numero_cuenta] = cuenta.to_dict()
                self.guardar_datos(datos)
                print(f"Cuenta {cuenta.numero_cuenta} creada correctamente.")
            else:
                print(f"Ya existe una cuenta con número '{numero_cuenta}'.")
        except Exception as error:
            print(f'Error inesperado al crear cuenta: {error}')

    def leer_cuenta(self, numero_cuenta):
        try:
            datos = self.leer_datos()
            if str(numero_cuenta) in datos:
                cuenta_data = datos[str(numero_cuenta)]
                if 'limite_descubierto' in cuenta_data:
                    cuenta = CuentaCorriente(**cuenta_data)
                else:
                    cuenta = CuentaAhorro(**cuenta_data)
                print(f'Cuenta encontrada con número {numero_cuenta}')
                return cuenta
            else:
                print(f'No se encontró cuenta con número {numero_cuenta}')
        except Exception as e:
            print(f'Error al leer cuenta: {e}')

    def actualizar_saldo(self, numero_cuenta, nuevo_saldo):
        try:
            datos = self.leer_datos()
            if str(numero_cuenta) in datos.keys():
                 datos[str(numero_cuenta)]['saldo'] = nuevo_saldo
                 self.guardar_datos(datos)
                 print(f'Saldo actualizado para la cuenta número: {numero_cuenta}')
            else:
                print(f'No se encontró cuenta con número: {numero_cuenta}')
        except Exception as e:
            print(f'Error al actualizar la cuenta: {e}')

    def eliminar_cuenta(self, numero_cuenta):
        try:
            datos = self.leer_datos()
            if str(numero_cuenta) in datos.keys():
                 del datos[str(numero_cuenta)]
                 self.guardar_datos(datos)
                 print(f'Cuenta número: {numero_cuenta} eliminada correctamente')
            else:
                print(f'No se encontró cuenta con número: {numero_cuenta}')
        except Exception as e:
            print(f'Error al eliminar la cuenta: {e}')
