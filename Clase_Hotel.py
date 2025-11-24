# Imports de funciones y librerias
from Clase_Habitacion import Habitacion
from datetime import date
from Clase_Escribir_txt import escribir_reserva, leer_reservas, eliminar_registro, eliminar_aut, mostrar_registros_eliminados, leer_eliminados
from google import genai
from getpass import getpass
from Conexion_DB import escribir_db, eliminar_reserva, eliminacion_aut, mostrar_reservas, insertar_habitaciones, escribir_historial, mostrar_historial



# Clase Hotel 
class Hotel:
    def __init__(self, nombre, cant_habitaciones, conexion):
        self.nombre = nombre
        self.cant_habitaciones = cant_habitaciones
        self.conexion = conexion
        self.habitaciones = []
        self.reservas = {}
        self.lugares = {}

        tipos = [("Simple", 25000), ("Matrimonial", 50000), ("Familiar", 100000)]
        cantidad_por_tipo = cant_habitaciones // len(tipos)  # divide las habitaciones por tipo

        for tipo, precio in tipos:
            for _ in range(cantidad_por_tipo):
                numero = len(self.habitaciones) + 1
                self.habitaciones.append(Habitacion(tipo, numero, precio))

        # Si sobran habitaciones (por ejemplo 10 no divisible por 3)
        while len(self.habitaciones) < cant_habitaciones:
            numero = len(self.habitaciones) + 1
            self.habitaciones.append(Habitacion("Familiar", numero, 100000))
        
        insertar_habitaciones(self.conexion, "tabla_habitaciones", self.habitaciones)

    
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
    
    def mostrar_todas_habitaciones(self):
        texto = ""
        for h in self.habitaciones:
            estado = "Ocupada" if h.ocupada else "Libre"
            texto += f"N°{h.numero} - {h.tipo} - ${h.precio} - Estado: {estado}\n"
        return texto
    

    # Funcion para realizar una reserva de habitacion
    def reservar_habitacion(self, cantidad_personas, confirmacion, nombre_cliente, dni, dia_ingreso, dia_salida):
        print(f"¡Bienvenido a {self.nombre}!")

        # Solicito la cantidad de personas
        # cantidad_personas = int(input("Ingrese la cantidad de personas a hospedar: "))

        # Validacion de habitacion segun la cantidad de personas
        if cantidad_personas == 1:
            print("Se sugiere reservar la habitación simple para una sola persona.")
            tipo = "Simple"
        elif cantidad_personas == 2:
            print("Se sugiere reservar la habitacion matrimonial para dos personas.")
            tipo = "Matrimonial"
        elif cantidad_personas > 2 and cantidad_personas <= 5:
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

        # confirmacion = input("Desea confirmar la operacion? si / no: ").lower()
        if confirmacion == True:
            # Solicito los datos del cliente
            # nombre_cliente = input("Ingrese su nombre y apellido: ").upper()
            # dni = input("Ingrese dni del titular de la reserva: ")
             # Solicito las fechas a reservar
            # dia_ingreso = input("Ingrese la fecha de ingreso al hotel (formato año-mes-día): ")
            # dia_salida = input("Ingrese la fecha de salida del hotel (formato año-mes-día): ")
        
            
            # Trasnsformo los datos de los dias de ingreso y salida
            dia_ingreso_dt = date.fromisoformat(dia_ingreso)
            dia_salida_dt = date.fromisoformat(dia_salida)
            # Calculo la diferencia de dias
            diferencia_dias = (dia_salida_dt - dia_ingreso_dt).days
            
            # Noches a Cobrar
            if diferencia_dias <= 0:
                # Si el ingreso y la salida son el mismo día o la salida es anterior.
                # Asumimos que si ingresan y salen el mismo día, se cobra 1 día/noche mínimo.
                noches_a_cobrar = 1
                       
                if diferencia_dias < 0:
                    print("Advertencia: La fecha de salida es anterior a la de ingreso. Se cobrará una noche mínima.")
                else:
                    print("Reserva de un día. Se cobrará el precio de una noche.")
                    
            else:
                        # Para el resto de los casos, se cobran las noches reales
                noches_a_cobrar = diferencia_dias

                    # Calcular el total
            monto_a_pagar = noches_a_cobrar * hab.precio

            if hab.reservar():
                self.reservas[dni] = {
                    "nombre": nombre_cliente,
                    "habitacion": hab.numero,
                    "tipo": hab.tipo,
                    "precio": hab.precio,
                    "ingreso": dia_ingreso,
                    "salida": dia_salida,
                    "total": monto_a_pagar
                } 
                # Guardo mis datos en variables para poder cargarlos en el txt
                registro = f"{nombre_cliente},{dni},{hab.tipo},{dia_ingreso},{dia_salida},{hab.precio}, {monto_a_pagar}"
                # Llamo a la funcion y escribo el archivo txt
                escribir_reserva("Hotel_Registro.txt", registro)
                escribir_db(self.conexion, "tabla_reservas", cantidad_personas, nombre_cliente, dni,hab.numero, hab.tipo, dia_ingreso, dia_salida, monto_a_pagar )
                # Muestro el mensaje con descripcion para confirmar la reserva
                print(f"Se registró la reserva de una habitacion {hab.tipo} a nombre de {nombre_cliente}, DNI {dni} desde {dia_ingreso} hasta {dia_salida}. El total a pagar es de ${monto_a_pagar} ")
                return nombre_cliente, dni, hab.tipo, dia_ingreso, dia_salida, hab.precio, monto_a_pagar
        elif confirmacion == False:
            print("Operación cancelada!")
            return
        
    def actualizar_estados(self):
        # Primero, resetear todas las habitaciones a libres
        for h in self.habitaciones:
            h.ocupada = False

        # Leer reservas actuales de la DB
        reservas_actuales = mostrar_reservas(self.conexion, "tabla_reservas")

        for reserva in reservas_actuales:
            num_hab = reserva['num_habitacion']
            # Marcar la habitación correspondiente como ocupada
            for h in self.habitaciones:
                if h.numero == num_hab:
                    h.ocupada = True
                    break


    def mostrar_reservas(self):
        reservas = mostrar_reservas(self.conexion, "tabla_reservas")

        texto = ""
        for fila in reservas:
            texto += (
                f"Cliente: {fila['nombre_cliente']} | "
                f"DNI: {fila['dni']} | "
                f"Personas: {fila['cantidad_personas']} | "
                f"Habitacion: {fila['num_habitacion']} ({fila['tipo_habitacion']}) | "
                f"Ingreso: {fila['fecha_de_ingreso']} | "
                f"Salida: {fila['fecha_de_salida']} | "
                f"Monto Total: ${fila['monto_a_pagar']}\n"
            )

        return texto if texto else "No hay reservas registradas."

    
    
    # Funcion para cancelar reserva
    def eliminar_reserva(self, dni_buscado):
        # dni_buscado = input("Ingrese el dni de la reserva a cancelar: ")
        eliminar_reserva(self.conexion, "tabla_reservas", dni_buscado)
        eliminar_registro("Hotel_Registro.txt", dni_buscado)
    
    # Funcion para eliminar las reservas de manera automatica una vez que se cumpla la fecha de salida
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

        # Escribo la DB historial
        escribir_historial(self.conexion, "tabla_reservas", "tabla_historial")

        # Elimino el registro del SQL
        eliminacion_aut(self.conexion, "tabla_reservas")

        # Actualizo el txt
        eliminar_aut("Hotel_Registro.txt", registros_actualizados)

        # Registro las eliminadas en un historial
        if eliminados:
            for res in eliminados:
                mostrar_registros_eliminados("Hotel_Registros_Eliminados.txt", res)
            print(f"Se registraron {len(eliminados)} reservas eliminadas en 'Hotel_Registros_Eliminados.txt'.")
        else:
            print("No había reservas con fecha de salida igual o anterior al día de hoy.")

    # Funcion para mostrar los registros eliminados del txt y base de datos principal
    def mostrar_eliminados(self):
        # Leer registros eliminados desde TXT y SQL
        historial_sql = mostrar_historial(self.conexion, "tabla_historial")

        texto = ""
    
        if historial_sql:
            for r in historial_sql:
                texto += (
                    f"Cliente: {r['nombre_cliente']} - DNI: {r['dni']}\n"
                    f"Habitación: {r['num_habitacion']} ({r['tipo_habitacion']})\n"
                    f"Ingreso: {r['fecha_de_ingreso']}  |  Salida: {r['fecha_de_salida']}\n"
                    f"Monto: ${r['monto_a_pagar']}\n"
                    f"Eliminado el: {r['fecha_eliminacion']}\n"
                    f"Motivo: {r['motivo_eliminacion']}\n"
                    f"{'-'*70}\n\n"
                )
        else:
            texto += "No hay registros en el historial de SQL.\n\n"

        return texto



    # Funcion de API GEMINI
    def api_gemini(self, pregunta):

        # Crea el cliente
        api_key = "AIzaSyBPY2AZbZTPcoV1LS-3h8UxNVcrHJNw5KE"
        client = genai.Client(api_key=api_key)

        # Pregunta al usuario
        # pregunta = input("Ingrese su pregunta: ")

        # Usar el modelo (acá model es un OBJETO, no un string)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=pregunta
        )

        # Muestra la respuesta
        #print("\n Respuesta:")
        #print(response.text)
        return response.text

