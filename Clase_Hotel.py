from Clase_Habitacion import Habitacion
from datetime import date
from Clase_Escribir_txt import escribir_reserva
from Clase_Escribir_txt import leer_reservas
from Clase_Escribir_txt import eliminar_registro
from google import genai
from getpass import getpass
from Clase_Escribir_txt import eliminar_aut
from Clase_Escribir_txt import mostrar_registros_eliminados
from Clase_Escribir_txt import leer_eliminados

class Hotel():
    def __init__ (self, nombre, cant_habitaciones):
        self.nombre = nombre
        self.cant_habitaciones = cant_habitaciones
        self.habitaciones = []
        self.reservas = {}
        self.lugares = {}
        # txt = Leer("Hotel_Registro.txt")
        
        # self.conexion = conexion

        # Creo las habitaciones con la capacidad del hotel
        for i in range(1, cant_habitaciones + 1):
            if i <= 1:
                tipo = "Simple"
                precio = 25000
            elif i <= 2:
                tipo = "Matrimonial"
                precio = 50000
            elif i <= 5:
                tipo = "Familiar"
                precio = 100000

            self.habitaciones.append(Habitacion(tipo, i, precio))
    
    # Muestro las habitaciones libres con sus descripciones
    def mostrar_disponibles(self):
        print("Habitaciones disponibles: ")
        disponibles = [h for h in self.habitaciones if not h.ocupada]
        if not disponibles:
            print("No hay habitaciones disponibles!")
        else:
            for h in disponibles:
                print(f"N°{h.numero} - {h.tipo} - ${h.precio}")
        return disponibles

    # Funcion para realizar una reserva de habitacion
    def reservar_habitacion(self):
        print(f"¡Bienvenido a {self.nombre}!")

        # Solicito la cantidad de personas
        cant_personas = int(input("Ingrese la cantidad de personas a hospedar: "))

        # Validacion de habitacion segun la cantidad de personas
        if cant_personas == 1:
            print("Se sugiere reservar la habitación simple para una sola persona.")
            tipo = "Simple"
        elif cant_personas == 2:
            print("Se sugiere reservar la habitacion matrimonial para dos personas.")
            tipo = "Matrimonial"
        elif cant_personas > 2 and cant_personas <= 5:
            print("Se sugiere reservar la habitacion familiar.")
            tipo = "Familiar"
        else:
            print("No hay habitaciones disponibles para esa cantidad de personas!")

        disponibles = [h for h in self.habitaciones if h.tipo == tipo and not h.ocupada]
        if not disponibles:
            print("No hay habitaciones disponibles de ese tipo.")
            return

        # Primera habitacion disponible
        hab = disponibles[0]

        confirmacion = input("Desea confirmar la operacion? si / no: ").lower()
        if confirmacion == "si":
            # Solicito los datos del cliente
            nombre_cliente = input("Ingrese su nombre y apellido: ").upper()
            dni = input("Ingrese dni del titular de la reserva: ")
             # Solicito las fechas a reservar
            dia_ingreso = input("Ingrese la fecha de ingreso al hotel (formato año-mes-día): ")
            dia_salida = input("Ingrese la fecha de salida del hotel (formato año-mes-día): ")
        elif confirmacion == "no":
            print("Operación cancelada!")

        if hab.reservar():
            self.reservas[dni] = {
                "nombre": nombre_cliente,
                "habitacion": hab.numero,
                "tipo": hab.tipo,
                "precio": hab.precio,
                "ingreso": dia_ingreso,
                "salida": dia_salida
            } 
            # Guardo mis datos en variables para poder cargarlos en el txt
            registro = f"{nombre_cliente},{dni},{hab.tipo},{dia_ingreso},{dia_salida},{hab.precio}"
            # Llamo a la funcion y escribo el archivo txt
            escribir_reserva("Hotel_Registro.txt", registro)
            # Muestro el mensaje con descripcion para confirmar la reserva
            print(f"Se registró la reserva de una habitacion {hab.tipo} a nombre de {nombre_cliente}, DNI {dni} desde {dia_ingreso} hasta {dia_salida} ")
            return nombre_cliente, dni, hab.tipo, dia_ingreso, dia_salida, hab.precio

    # Funcion para mostrar las reservas cargadas en DB
    def mostrar_reservas(self):
        reservas_actuales = leer_reservas("Hotel_Registro.txt")

        if not reservas_actuales:
            print("No hay reservas registradas")
            return

        for i, reserva in enumerate(reservas_actuales, start=1):
            if len(reserva) >= 6:
                nombre, dni, tipo, ingreso, salida, precio = reserva
                print(f"{i}. {nombre} (DNI {dni}) - {tipo} | Ingreso: {ingreso} | Salida: {salida} | Precio: ${precio}")
    
    # Funcion para eliminar reserva
    def eliminar_reserva(self):
        dni = input("Ingrese el dni de la reserva a cancelar: ")
        eliminar_registro("Hotel_Registro.txt", dni)
    
    # Funcion para eliminar las reservas una vez que se cumpla la fecha de salida
    def eliminacion_automatica(self):
        datos_actuales = leer_reservas("Hotel_Registro.txt")
        registros_actualizados = []
        hoy = date.today()
        eliminados = []

        for reserva in datos_actuales:
            fecha_salida_str = reserva[4].strip()
            try:
                año, mes, dia = map(int, fecha_salida_str.split("-"))
                fecha_salida_dt = date(año, mes, dia)
            except ValueError:
                print(f"Formato de fecha inválido en registro: {reserva}")
                registros_actualizados.append(reserva)
                continue

            # Si la fecha de salida es hoy o ya pasó
            if fecha_salida_dt <= hoy:
                print(f"La reserva de {reserva[0]}, DNI {reserva[1]} fue eliminada automáticamente (fin del periodo).")
                eliminados.append(reserva)
            else:
                registros_actualizados.append(reserva)

        # Sobrescribo el archivo de reservas con las que quedan activas
        eliminar_aut("Hotel_Registro.txt", registros_actualizados)

        # Registro las eliminadas en un historial
        if eliminados:
            for res in eliminados:
                mostrar_registros_eliminados("Hotel_Registros_Eliminados.txt", res)
            print(f"Se registraron {len(eliminados)} reservas eliminadas en 'Hotel_Registros_Eliminados.txt'.")
        else:
            print("No había reservas con fecha de salida igual o anterior al día de hoy.")

    def mostrar_eliminados(self):
        eliminados = leer_eliminados("Hotel_Registros_Eliminados.txt")

        if not eliminados:
            print("No hay reservas registradas")
            return

        for i, reserva in enumerate(eliminados, start=1):
            if len(reserva) >= 6:
                nombre, dni, tipo, ingreso, salida, precio = reserva
                print(f"{i}. {nombre} (DNI {dni}) - {tipo} | Ingreso: {ingreso} | Salida: {salida} | Precio: ${precio}")
        return eliminados


    # Funcion de API GEMINI
    def api_gemini(self):

        # Crea el cliente
        client = genai.Client(api_key=getpass("Ingrese API key de Gemini: "))

        # Pregunta al usuario
        pregunta = input("Ingrese su pregunta: ")

        # Usar el modelo (acá model es un OBJETO, no un string)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=pregunta
        )

        # Muestra la respuesta
        print("\n Respuesta:")
        print(response.text)

        

# AIzaSyBPY2AZbZTPcoV1LS-3h8UxNVcrHJNw5KE
