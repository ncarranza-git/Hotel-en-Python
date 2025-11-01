import pymysql
import getpass

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

def crear_tabla(conexion_db, tabla_reservas):
    cursor = conexion_db.cursor()
    sql = f""" CREATE TABLE IF NOT EXISTS {tabla_reservas} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        cant_personas INT (10) NOT NULL,
        nombre_cliente  VARCHAR (50) NOT NULL,
        dni VARCHAR (50) NOT NULL,
        fecha_de_ingreso DATE NOT NULL,
        fecha_de_salida DATE NOT NULL
    );
    """
    cursor.execute(sql)
    print("Se creo la tabla correctamente!!")

def escribir_db(conexion_db, tabla_reservas, cant_personas, nombre_cliente, dni, dia_ingreso, dia_salida ):
    cursor = conexion_db.cursor()
    sql = f"""INSERT INTO {tabla_reservas} 
             (cant_personas, nombre_cliente, dia_ingreso, dia_salida)
             VALUES (%s, %s, %s, %s)"""
    cursor.execute(sql, (cant_personas, nombre_cliente, dni, dia_ingreso, dia_salida))
    conexion_db.commit()
    print("Se cargaron los datos correctamente en la DB!!")
    