def escribir_reserva(nombre_archivo, registro):  
    with open(nombre_archivo, "a", encoding="utf-8") as archivo:
        archivo.write(registro + "\n")  # Agrega salto de línea al final

def leer_reservas(nombre_archivo):
    with open("Hotel_Registro.txt", "r", encoding="utf-8") as archivo:  # Abre y asegura el cierre automático
        texto = archivo.readlines()  # Lee todas las líneas en una lista
        reservas_hotel = []
        for linea in texto:
            aux = linea.split(",")
            reservas_hotel.append(aux)
        return reservas_hotel

def eliminar_registro(nombre_archivo, dni):
   nuevo_registro = leer_reservas(nombre_archivo)
   encontrado = False

   for registro in nuevo_registro:
        if registro[1] == dni:
            print(f"Se quitó el registro con DNI: {dni}")
            nuevo_registro.remove(registro)
            encontrado = True
        elif registro[1] != dni:
             print("No se encontró el dni dentro del registro")

        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            for lista in nuevo_registro:
                registro = ",".join(lista).strip()
                archivo.write(registro+"\n")

def eliminar_aut(registros_actualizados, archivo="Hotel_Registro.txt"):
    with open("Hotel_Registro.txt", "w", encoding="utf-8") as archivo:
        for lista in registros_actualizados:
            linea = ",".join([campo.strip() for campo in lista])
            archivo.write(linea + "\n")

def mostrar_registros_eliminados(registro):
    with open("Hotel_Registros_Eliminados.txt", "a", encoding="utf-8") as archivo:
        linea = ",".join([str(campo).strip() for campo in registro])
        archivo.write(linea + "\n")


def leer_eliminados(nombre_archivo):
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        texto = archivo.readlines()
        reservas_eliminadas = []
        for linea in texto:
            aux = linea.strip().split(",")  # <- strip() para quitar \n
            reservas_eliminadas.append(aux)
        return reservas_eliminadas
