# Imports necesarios
from Clase_Hotel import Hotel
from Conexion_DB import conectar, crear_tabla
from Hotel_GUI import HotelGUI

IP_DB = '127.0.0.1'
USER_DB = 'root' 
PORT_DB = 3307

conexion = conectar(ip=IP_DB, usuario=USER_DB, puerto=PORT_DB)

if not conexion:
    print("Fallo al conectar a la Base de Datos. El programa no puede continuar.")
        

crear_tabla(conexion, "tabla_habitaciones", "tabla_reservas", "tabla_historial")

hotel1 = Hotel('Mi Hotel en Python', 10, conexion)

app = HotelGUI(hotel1)

# print(f"Bienvenidos a {hotel1.nombre}")

# print("1: Realizar una reserva")
# print("2: Mostrar reservas registradas")
# print("3: Cancelar reserva")
# print("4: IA de consulta")
# print("5: Mostrar habitaciones disponibles")
# print("6: Mostrar historial de reservas eliminadas")
# print("7: Salir")

# opcion = int(input("Indique la opcion que desea realizar: "))

# if opcion == 1:
#     hotel1.eliminacion_automatica()
#     hotel1.reservar_habitacion()
# elif opcion == 2:
#     hotel1.eliminacion_automatica()
#     hotel1.mostrar_reservas()
# elif opcion == 3:
#     hotel1.eliminacion_automatica()
#     hotel1.eliminar_reserva()
# elif opcion == 4:
#     hotel1.api_gemini()
# elif opcion == 5:
#     hotel1.mostrar_disponibles()
# elif opcion == 6:
#     hotel1.mostrar_eliminados()
# elif opcion == 7:
#     print("Gracias por uitilizar el sistema. Hasta luego!")
#     pass
# else:
#     print("Error, opcion fuera de rango!")

