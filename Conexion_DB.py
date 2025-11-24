import pymysql
import getpass
import sqlite3

# Conexion con la base de datos 
def conectar(ip,usuario,puerto):
    connection = pymysql.connect(host=ip,
                                user=usuario,
                                password=getpass.getpass("Ingrese la contraseña: "),
                                port=puerto,
                                database='db_hotel',
                                cursorclass=pymysql.cursors.DictCursor)
    print("Conectado a la DB!")
    return connection

# Funcion para crear las tablas en donde se almacenan los datos 
def crear_tabla(conexion_db, tabla_habitaciones, tabla_reservas, tabla_historial):
    cursor = conexion_db.cursor()
    sql_habitaciones = f"""CREATE TABLE IF NOT EXISTS {tabla_habitaciones} (
        numero INT PRIMARY KEY,
        tipo VARCHAR(50) NOT NULL,
        precio DECIMAL(10, 2) NOT NULL,
        # 'Disponible', 'Ocupada', 'Mantenimiento'
        estado VARCHAR(50) NOT NULL DEFAULT 'Disponible'
    );
    
    """
    sql_reservas = f""" CREATE TABLE IF NOT EXISTS {tabla_reservas} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        cantidad_personas INT NOT NULL,
        nombre_cliente  VARCHAR (50) NOT NULL,
        dni VARCHAR (50) NOT NULL,
        num_habitacion INT NOT NULL,
        tipo_habitacion VARCHAR(50) NOT NULL,
        fecha_de_ingreso DATE NOT NULL,
        fecha_de_salida DATE NOT NULL,
        monto_a_pagar DECIMAL (10,2) NOT NULL,

        FOREIGN KEY (num_habitacion) REFERENCES {tabla_habitaciones}(numero)
    );
    """
    sql_historial = f""" CREATE TABLE IF NOT EXISTS {tabla_historial} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        cantidad_personas INT NOT NULL,
        nombre_cliente  VARCHAR (50) NOT NULL,
        dni VARCHAR (50) NOT NULL, 
        num_habitacion INT NOT NULL,
        tipo_habitacion VARCHAR(50) NOT NULL,
        fecha_de_ingreso DATE NOT NULL,
        fecha_de_salida DATE NOT NULL,
        monto_a_pagar DECIMAL (10,2) NOT NULL,
        fecha_eliminacion DATE NOT NULL,
        motivo_eliminacion VARCHAR(100)
    );
    """
    cursor.execute(sql_habitaciones)
    cursor.execute(sql_reservas) 
    cursor.execute(sql_historial)
    print("Se creo la tabla correctamente!!")

# Funcion para insertar los datos en la tabla del SQL
def escribir_db(conexion_db, tabla_reservas, cantidad_personas, nombre_cliente, dni, num_habitacion, tipo_habitacion, dia_ingreso, dia_salida, monto_a_pagar ):
    cursor = conexion_db.cursor()
    sql = f"""INSERT INTO {tabla_reservas} 
             (cantidad_personas, nombre_cliente, dni, num_habitacion, tipo_habitacion, fecha_de_ingreso, fecha_de_salida, monto_a_pagar)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, (cantidad_personas, nombre_cliente, dni, num_habitacion, tipo_habitacion, dia_ingreso, dia_salida, monto_a_pagar))
    conexion_db.commit()
    print("Se cargaron los datos correctamente en la DB!!")

# Funcion para cancelar y borrar un registro de la tabla del SQL
def eliminar_reserva(conexion_db, tabla_reservas, dni_buscado):
    cursor = conexion_db.cursor()
    sql = f""" DELETE FROM {tabla_reservas}
                WHERE dni = %s """
    cursor.execute(sql, (dni_buscado,))
    conexion_db.commit()
    print("Se eliminó la reserva correctamente!")

# Funcion para mostrar los registros que tiene la tabla de reservas
def mostrar_reservas(conexion_db, tabla_reservas):
    with conexion_db.cursor() as cursor:
        sql = f""" SELECT * FROM {tabla_reservas}"""
        cursor.execute(sql)
        resultado = cursor.fetchall()
        return resultado

# Funcion para eliminar de manera automatica un registro de la tabla en SQL una vez que se cumpla el dia de salida    
def eliminacion_aut(conexion_db, tabla_reservas):
    cursor = conexion_db.cursor()
    sql = f""" DELETE FROM {tabla_reservas}
                WHERE fecha_de_salida <= CURDATE() """
    cursor.execute(sql)
    conexion_db.commit()
    print("Se eliminó reserva automaticamente por fin de período")

# Funcion para insertar los datos de las habitaciones con sus atributos a la tabla del SQL
def insertar_habitaciones(conexion_db, nombre_tabla, lista_habitaciones):
    cursor = conexion_db.cursor()

    # Verifica si la tabla ya tiene habitaciones
    cursor.execute(f"SELECT numero FROM {nombre_tabla}")
    existentes = {fila["numero"] for fila in cursor.fetchall()}

    # Insertar nuevas habitaciones (solo si no existen)
    sql_insert = f"""
        INSERT INTO {nombre_tabla} (numero, tipo, precio, estado)
        VALUES (%s, %s, %s, %s)
    """

    # Actualizar habitaciones existentes sin borrar (seguro)
    sql_update = f"""
        UPDATE {nombre_tabla}
        SET tipo = %s, precio = %s
        WHERE numero = %s
    """

    for h in lista_habitaciones:
        if h.numero not in existentes:
            # Insertar solo si NO existe
            cursor.execute(sql_insert, (h.numero, h.tipo, h.precio, "Disponible"))
        else:
            # Actualizar datos si ya existe (no rompe FK)
            cursor.execute(sql_update, (h.tipo, h.precio, h.numero))

    conexion_db.commit()
    print("Habitaciones sincronizadas con la DB (sin borrar registros).")

def escribir_historial(conexion_db, tabla_reservas, tabla_historial):
    # Buscar reservas vencidas
    cursor = conexion_db.cursor()
    cursor.execute(f"SELECT * FROM {tabla_reservas} WHERE fecha_de_salida <= CURDATE()")
    reservas = cursor.fetchall()

    # Pasarlas al historial antes de eliminar
    for r in reservas:
        sql_hist = f"""
            INSERT INTO {tabla_historial}
            (cantidad_personas, nombre_cliente, dni, num_habitacion, tipo_habitacion,
            fecha_de_ingreso, fecha_de_salida, monto_a_pagar, fecha_eliminacion, motivo_eliminacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURDATE(), %s)
        """
        cursor.execute(sql_hist, (
            r["cantidad_personas"],
            r["nombre_cliente"],
            r["dni"],
            r["num_habitacion"],
            r["tipo_habitacion"],
            r["fecha_de_ingreso"],
            r["fecha_de_salida"],
            r["monto_a_pagar"],
            "Eliminación automática por fecha"
        ))
    conexion_db.commit()

def mostrar_historial(conexion_db, tabla_historial):
    conexion_db.row_factory = sqlite3.Row
    cursor = conexion_db.cursor()
    cursor.execute(f"SELECT * FROM {tabla_historial} ORDER BY fecha_eliminacion DESC")
    return [dict(row) for row in cursor.fetchall()]
