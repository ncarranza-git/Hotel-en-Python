Descripción General del Sistema
"Mi Hotel en Python" es una aplicación de escritorio diseñada para la gestión de reservas de un hotel. Utiliza una interfaz gráfica (GUI) construida con Tkinter para la interacción con el usuario, y persiste los datos en una base de datos MySQL y archivos de texto (.txt) para los registros actuales e históricos del Hotel.

Requisitos del Sistema 
Software Requerido: Python.
Librerías Python: Tkinter para la GUI, pymysql, sqlite3, Google-genai.
Base de Datos: Servidor MySQL activo (el código requiere una conexión constante a la base de datos ‘db_hotel’).
API key: clave de API de Google Gemini para la funcionalidad de la IA.
Sistema Operativo: compatible con cualquier Sistema Operativo que soporte Python.

Configuración Inicial - Primera Vez
La conexión a la base de datos se realiza al crear la instancia de Hotel en tu script principal, llamando a la función conectar de Conexion_DB.py. Asegúrate de tener las credenciales correctas.
1.	Conexión DB: El sistema solicitará la contraseña de la base de datos al inicio (usa getpass para ocultarla).
2.	Creación de Tablas: Automáticamente, el sistema crea tres tablas si no existen: tabla_habitaciones, tabla_reservas, y tabla_historial.
3.	Carga de Habitaciones: Las habitaciones iniciales (Simple, Matrimonial, Familiar) se cargan o actualizan automáticamente en la tabla_habitaciones de MySQL al iniciar el objeto Hotel, según los atributos que se definan al mismo.

Inicio del Programa
Para iniciar el sistema, se debe ejecutar el archivo Main.py

Menú Principal
La ventana principal ofrece las siguientes opciones para gestionar el hotel:
•	Realizar Reserva
•	Mostrar Habitaciones
•	Cancelar Reserva
•	IA Gemini
•	Mostrar Reservas Registradas
•	Historial de Reservas
•	Salir

Funcionalidades Principales
1. Realizar Reserva 
Esta función guía al usuario a través de dos pasos para registrar una nueva reserva.

    Paso 1: Cantidad de Personas
    o	Ingrese el número de personas a hospedar.
    o	El sistema sugiere automáticamente un tipo de habitación (Simple (1), Matrimonial (2), Familiar (3-5)) basado en esta cantidad.

    Paso 2: Datos Personales y Fechas
    o	Ingrese Nombre y Apellido, DNI del titular.
    o	Ingrese la Fecha de Ingreso y Fecha de Salida en formato AAAA-MM-DD (Ej: 2026-01-20).
    o	Al presionar "Guardar Reserva":
        El sistema busca la primera habitación Libre del tipo sugerido.
        Calcula el Monto Total (Noches a Cobrar x Precio de Habitación).
        Marca la habitación como Ocupada.
        Guarda el registro en el archivo de texto Hotel_Registro.txt y en la tabla ‘tabla_reservas’ de MySQL.

2. Mostrar Habitaciones 
Muestra el estado actual de todas las habitaciones del hotel.
•	El sistema llama a hotel.actualizar_estados() para sincronizar los estados (Ocupada/Libre) de las habitaciones internas de Python con la lista de reservas activas en la base de datos MySQL.
•	Presenta una lista detallada con el Número, Tipo, Precio y el Estado (Libre u Ocupada) de cada habitación.

3. Cancelar Reserva 
Permite al usuario eliminar una reserva activa de forma manual.
•	Se le solicita el DNI de la reserva a cancelar.
•	Al confirmar, la reserva se elimina de la tabla tabla_reservas de MySQL (usando eliminar_reserva) y del archivo de texto Hotel_Registro.txt.

4. IA Gemini 
Permite realizar consultas generales utilizando la API de Google Gemini (requiere que la clave de API sea válida).
•	Se abre una ventana para que el usuario ingrese una pregunta.
•	El sistema envía la pregunta a la API y muestra la respuesta generada por el modelo.

5. Mostrar Reservas Registradas 
Recupera y muestra todas las reservas actualmente activas.
•	La información se obtiene directamente de la tabla ‘tabla_reservas’ de MySQL mediante la función mostrar_reservas.
•	Muestra el DNI, Cliente, Habitación, Fechas y el Monto Total de cada reserva.

6. Historial de Reservas (Registros Eliminados) 
Muestra el registro de todas las reservas que han sido finalizadas.
•	La información proviene de la tabla tabla_historial de MySQL.
•	Incluye detalles de la reserva original, la fecha de eliminación y el motivo de la eliminación ("Eliminación automática por fecha") para constar de que el cliente utilizó el servicio del hotel.
Proceso Automático de Limpieza: Cada vez que se intenta hacer una reserva o se accede a la ventana de datos personales, el sistema ejecuta eliminacion_automatica(). Este proceso:
1.	Identifica reservas cuya fecha de salida es igual o anterior al día de hoy.
2.	Mueve esos registros a la tabla tabla_historial de MySQL.
3.	Elimina esos registros de la tabla tabla_reservas de MySQL.
4.	Actualiza los archivos de texto correspondientes.
