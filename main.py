import psycopg2
from psycopg2 import connect, Error

def connection():
    try:
        connection = connect(host='localhost',database='BaseTaller2',user='postgres', password='aparatos', port='5432')
        connection.autocommit = True # Autocommit es un método que permite que cada sentencia sql se ejecute en una transacción
        return connection
    except(Exception, Error) as error:
        print("Error: %s" % error)
        connection.rollback() # Reversion de una transaccion incompleta o fallida
        cursor.close() # Cerramos el objetos cursor para (Cursor permite ejecutar los comandos sql)
        return None
    

def select_query(query, data=[]):
    try:
        if connection() and query != '' and data == []:
            cursor = connection().cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        elif connection() and query != '' and data != []:
            cursor = connection().cursor()
            cursor.execute(query, tuple(data))
            result = cursor.fetchall()
            return result
    except(Exception, Error) as error:
        print("Error: %s" % error)
        connection.rollback()

def create_users_table():
    try:
        conn = connection()
        cursor = conn.cursor()
        create_table_query = """
        CREATE TABLE users (
            username text UNIQUE,
            password text
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
    except psycopg2.Error as e:
        print("Error al crear la tabla de usuarios:", e)
    finally:
        if conn:
            conn.close()

# Función para crear la tabla de productos
def create_products_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS productos (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(255),
            descripcion TEXT,
            precio DECIMAL,
            cantidad_stock INT
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Tabla de productos creada exitosamente.")
    except psycopg2.Error as e:
        print("Error al crear la tabla de productos:", e)

# Función para crear la tabla de ventas
def create_ventas_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS ventas (
            id SERIAL PRIMARY KEY,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            cliente_id INT,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Tabla de ventas creada exitosamente.")
    except psycopg2.Error as e:
        print("Error al crear la tabla de ventas:", e)

# Función para crear la tabla de clientes
def create_clientes_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS clientes (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(255),
            direccion TEXT,
            email VARCHAR(255) UNIQUE
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Tabla de clientes creada exitosamente.")
    except psycopg2.Error as e:
        print("Error al crear la tabla de clientes:", e)

# Función para crear la tabla de inventario
def create_inventario_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS inventario (
            id SERIAL PRIMARY KEY,
            producto_id INT,
            cantidad_stock INT,
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Tabla de inventario creada exitosamente.")
    except psycopg2.Error as e:
        print("Error al crear la tabla de inventario:", e)

def register_new_user(conn):
    username = input("Ingrese un nombre de usuario nuevo: ")
    password = input("Ingrese una contraseña nueva: ")
    try:
        insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor = conn.cursor()
        cursor.execute(insert_query, (username, password))
        conn.commit()
        print("Usuario registrado exitosamente.")
    except psycopg2.Error as e:
        print("Error al registrar usuario:", e)


def login():
    username = input("Ingrese su nombre de usuario: ")
    password = input("Ingrese su contraseña: ")
    try:
        conn = connection()
        select_query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor = conn.cursor()
        cursor.execute(select_query, (username, password))
        user = cursor.fetchone()
        if user:
            print("Sesión iniciada.")
        else:
            print("Usuario no existe. Por favor, regístrese.")
            register_new_user(conn)
    except psycopg2.Error as e:
        print("Error al iniciar sesión:", e)
    finally:
        if conn:
            conn.close()

create_users_table()

admin_username = "camilo@tienda.com"
admin_password = "camilo@7720"

if connection():
    login()
