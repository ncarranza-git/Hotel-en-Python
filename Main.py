from Clase_Hotel import Hotel

hotel1 = Hotel('Las Vegas Hotel', 100)


print("1: Realizar una reserva")
print("2: Mostrar reservas registradas")
print("3: Cancelar reserva")
print("4: IA de consulta")
print("5: Mostrar habitaciones disponibles")


# hotel1.eliminacion_automatica()

opcion = int(input("Indique la opcion que desea realizar: "))

if opcion == 1:
    hotel1.reservar_habitacion()
elif opcion == 2:
    hotel1.mostrar_reservas()
elif opcion == 3:
    hotel1.eliminar_reserva()
elif opcion == 4:
    hotel1.api_gemini()
elif opcion == 5:
    hotel1.mostrar_disponibles()




