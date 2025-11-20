# Funcion para escribir los datos en el txt
def escribir_reserva(nombre_archivo, registro):  
    with open("Hotel_Registro.txt", "a", encoding="utf-8") as archivo:
        archivo.write(registro + "\n")  

# Funcion para leer los datos registrados en el txt
def leer_reservas(nombre_archivo):
    with open("Hotel_Registro.txt", "r", encoding="utf-8") as archivo:  
        texto = archivo.readlines()  
        reservas_hotel = []
        for linea in texto:
            aux = linea.split(",")
            reservas_hotel.append(aux)
        return reservas_hotel

# Funcion para cancelar una reserva
def eliminar_registro(nombre_archivo, dni_buscado):
   nuevo_registro = leer_reservas(nombre_archivo)
   encontrado = False

   for registro in nuevo_registro:
        if registro[1] == dni_buscado:
            print(f"Se quitó el registro con DNI: {dni_buscado}")
            nuevo_registro.remove(registro)
            encontrado = True
        elif registro[1] != dni_buscado:
             print("No se encontró el dni dentro del registro")

        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            for lista in nuevo_registro:
                registro = ",".join(lista).strip()
                archivo.write(registro+"\n")

# Funcion para eliminar los registros de manera automatica, cuando se cumpla el dia de salida
def eliminar_aut(nombre_archivo, registros_actualizados):
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        for lista in registros_actualizados:
            linea = ",".join(lista).strip()
            archivo.write(linea + "\n")

# Funcion para mostrar los registros que fueron eliminados del txt principal
def mostrar_registros_eliminados(nombre_archivo, registro):
    with open("Hotel_Registros_Eliminados.txt", "a", encoding="utf-8") as archivo:
        linea = ",".join([str(campo).strip() for campo in registro])
        archivo.write(linea + "\n")

# Funcion para leer los registros eliminados 
def leer_eliminados(nombre_archivo):
    with open("Hotel_Registros_Eliminados.txt", "r", encoding="utf-8") as archivo:
        texto = archivo.readlines()
        reservas_eliminadas = []
        for linea in texto:
            aux = linea.strip().split(",")  
            reservas_eliminadas.append(aux)
        return reservas_eliminadas
