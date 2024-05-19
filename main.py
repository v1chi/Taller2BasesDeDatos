import psycopg2
from psycopg2 import connect, Error
import re

#Establecer conexión con la base de datos
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
    
#Función para crear la tabla de usuarios
def create_users_table():
    try:
        conn = connection()
        cursor = conn.cursor()
        create_table_query = """
        CREATE TABLE if not exists usuarios (
            username text primary key,
            password text NOT NULL,
            role text NOT NULL
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        print("Tabla de usuarios creada")
    except psycopg2.Error as e:
        print("Error al crear la tabla de usuarios:", e)
    finally:
        if conn:
            conn.close()

# Función para crear la tabla de productos
def create_products_table():
    try:
        cursor = connection().cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS productos (
            nombre text primary key,
            descripcion text NOT NULL,
            precio int NOT NULL,
            cantidad_stock int NOT NULL
        );
        """
        cursor.execute(create_table_query)
        connection().commit()
        print("Tabla de productos creada exitosamente.")
    except psycopg2.Error as e:
        print("Error al crear la tabla de productos:", e)

# Función para crear la tabla de ventas
def create_ventas_table():
    try:
        cursor = connection().cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS ventas (
            id int PRIMARY KEY,
            cliente text REFERENCES clientes(username) NOT NULL,
            producto text references productos(nombre) NOT NULL,
            cantidad int NOT NULL
        );
        """
        cursor.execute(create_table_query)
        connection().commit()
        print("Tabla de ventas creada exitosamente.")
    except psycopg2.Error as e:
        print("Error al crear la tabla de ventas:", e)

# Función para crear la tabla de clientes
def create_clientes_table():
    try:
        cursor = connection().cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS clientes (
            username text primary key references usuarios(username),
            nombre text NOT NULL,
            direccion TEXT NOT NULL,
            email text NOT NULL
        );
        """
        cursor.execute(create_table_query)
        connection().commit()
        print("Tabla de clientes creada exitosamente.")
    except psycopg2.Error as e:
        print("Error al crear la tabla de clientes:", e)

#Funcion para verificar si la contraseña es válida
def is_valid_password(password):
    # La contraseña debe tener entre 6 y 8 caracteres
    if len(password) < 6 or len(password) > 8:
        return False
    # Al menos una letra mayúscula
    if not re.search("[A-Z]", password):
        return False
    #n Al menos un número 
    if not re.search("[0-9]", password):
        return False
    # Al menos un carácter especial
    if not re.search("[^A-Za-z0-9]", password):
        return False
    return True

#Ingresar un cliente en la base de datos
def register_client(username, email, direccion, nombre, conn):
    try:
        insert_query = "INSERT INTO clientes (username, nombre, email, direccion) VALUES (%s, %s, %s, %s)"
        cursor = conn.cursor()
        cursor.execute(insert_query, (username, nombre, email, direccion))
        conn.commit()
        print("Cliente registrado exitosamente.")
    except psycopg2.Error as e:
        print("Error al registrar cliente:", e)
    finally:
        if conn:
            conn.close()

#Registrar un usuario en la base de datos
def register_new_user(conn):
    #Se pide el nombre de usuario, contraseña y rol del usuario
    username = input("Ingrese un nombre de usuario: ")
    password = input("Ingrese una contraseña: ")
    role = input("Ingrese el rol (administrador/cliente): ")

    try:
        #Si la contraseña no es válida, se indica que hubi un error
        if not is_valid_password(password):
            print("La contraseña no cumple con los requisitos.")
            return
        #Si la contraseña es válida, se registra el usuario
        if role != "cliente" and role != "administrador":
            print("El rol no es valido")
            return

        insert_query = "INSERT INTO usuarios (username, password, role) VALUES (%s, %s, %s)"
        cursor = conn.cursor()
        cursor.execute(insert_query, (username, password, role))
        conn.commit()
        print("Usuario registrado exitosamente.")

        #Además, si el usuario es de tipo cliente, se pide su nombre y sus datos de contacto y se registra como cliente
        if role == "cliente":
            nombre = input("Ingrese su nombre: ")
            email = input("Ingrese su email: ")
            direccion = input("Ingrese su dirección: ")
            register_client(username, email, direccion, nombre, conn)
    except psycopg2.Error as e:
        print("Error al registrar usuario:", e) 

#Inicio de sesion
def login():
    username = input("Ingrese su nombre de usuario: ")
    password = input("Ingrese su contraseña: ")
    try:
        conn = connection()
        select_query = "SELECT * FROM usuarios WHERE username = %s AND password = %s"
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



if connection():
    """
    #Crear tablas:
    create_users_table()
    create_clientes_table()
    create_products_table()
    create_ventas_table()

    #Añadir a la tabla de usuarios a camilo@tienda.com:
    insert_query = "INSERT INTO usuarios (username, password, role) VALUES (%s, %s, %s)"
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(insert_query, ("camilo@tienda.com", "camilo@7720", "administrador"))
    conn.commit()
    """
    login()
