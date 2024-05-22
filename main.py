import psycopg2
from psycopg2 import connect, Error
import re

#Establecer conexión con la base de datos
def connection():
    try:
        connection = connect(host='localhost',database='BaseTaller2',user='postgres', password='postgres', port='5432')
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
        conn = connection()
        cursor = conn.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS productos (
            nombre text primary key,
            descripcion text NOT NULL,
            precio int NOT NULL,
            cantidad_stock int NOT NULL
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        print("Tabla de productos creada exitosamente.")
    except psycopg2.Error as e:
        print("Error al crear la tabla de productos:", e)

# Función para crear la tabla de ventas
def create_ventas_table():
    try:
        conn = connection()
        cursor = conn.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS ventas (
            id int PRIMARY KEY,
            cliente text REFERENCES clientes(username),
            producto text references productos(nombre) NOT NULL,
            cantidad int NOT NULL
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        print("Tabla de ventas creada exitosamente.")
    except psycopg2.Error as e:
        print("Error al crear la tabla de ventas:", e)

# Función para crear la tabla de clientes
def create_clientes_table():
    try:
        conn = connection()
        cursor = conn.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS clientes (
            username text primary key references usuarios(username),
            nombre text NOT NULL,
            direccion TEXT NOT NULL,
            email text NOT NULL
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
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
def register_client(username, email, direccion, nombre):
    try:
        insert_query = "INSERT INTO clientes (username, nombre, email, direccion) VALUES (%s, %s, %s, %s)"
        conn = connection()
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
def register_new_user():
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
        conn = connection()
        cursor = conn.cursor()
        cursor.execute(insert_query, (username, password, role))
        conn.commit()
        print("Usuario registrado exitosamente.")

        #Además, si el usuario es de tipo cliente, se pide su nombre y sus datos de contacto y se registra como cliente
        if role == "cliente":
            nombre = input("Ingrese su nombre: ")
            email = input("Ingrese su email: ")
            direccion = input("Ingrese su dirección: ")
            register_client(username, email, direccion, nombre)
    except psycopg2.Error as e:
        print("Error al registrar usuario:", e) 

#Registrar un nuevo producto
def registrar_producto():
    nombre = input("Ingrese el nombre del producto")
    descripcion = input("Ingrese la descripcion del producto")
    precio = input("Ingrese el precio del producto")
    cantidad_stock = input("Ingrese la cantidad de stock del producto")

    try:
        if not precio.isdigit() and not cantidad_stock.isdigit():
            print("Ingrese valores correctos para el precio y el stock (tienen que ser numeros enteros)")
            return
        insert_query = "INSERT INTO productos (nombre, descripcion, precio, cantidad_stock) VALUES (%s, %s, %s, %s)"
        conn = connection()
        cursor = conn.cursor()
        cursor.execute(insert_query, (nombre, descripcion, precio, cantidad_stock))
        connection().commit()
        print("Producto registrado exitosamente.")
    except psycopg2.Error as e:
        print("Error al registrar prodructo:", e)
    finally:
        if conn:
            conn.close()

#Obtener el ultimo id asignado a una venta
def obtener_ultimo_id():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM ventas;")
    ultimo_id = cursor.fetchone()[0]
    conn.close()
    return ultimo_id if ultimo_id is not None else 0

#Registrar una venta
def registrar_venta(producto, cantidad, cliente=None):
    try:
        conn = connection()
        cursor = conn.cursor()
        # Verificar si el producto existe y hay suficiente cantidad en stock
        select_query = "SELECT cantidad_stock FROM productos WHERE nombre = %s"
        cursor.execute(select_query, (producto,))
        cantidad_stock = cursor.fetchone()
        
        if cantidad_stock and cantidad_stock[0] >= cantidad:
            # Restar la cantidad vendida del stock del producto
            update_query = "UPDATE productos SET cantidad_stock = cantidad_stock - %s WHERE nombre = %s"
            cursor.execute(update_query, (cantidad, producto))

            nuevo_id = obtener_ultimo_id() + 1
            
            # Insertar la venta en la tabla de ventas
            insert_query = "INSERT INTO ventas (id, producto, cantidad, cliente) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (nuevo_id, producto, cantidad, cliente))
            conn.commit()
            print("Venta registrada exitosamente.")
        else:
            print("Producto no disponible.")
        
    except psycopg2.Error as e:
        print("Error al registrar venta:", e)
    finally:
        if conn:
            conn.close()

#Ver informacion de un producto
def ver_info_producto():
    try:
        conn = connection()
        cursor = conn.cursor()
        producto = input("Ingrese el nombre del producto: ")

        # Consulta para obtener la información del producto
        query = "SELECT nombre, descripcion, precio, cantidad_stock FROM productos WHERE nombre = %s"
        cursor.execute(query, (producto,))
        producto_info = cursor.fetchone()

        if producto_info:
            nombre, descripcion, precio, cantidad_stock = producto_info
            print(f"Nombre: {nombre}")
            print(f"Descripción: {descripcion}")
            print(f"Precio: {precio}")
            print(f"Cantidad en stock: {cantidad_stock}")
        else:
            print("Producto no encontrado.")

    except psycopg2.Error as e:
        print("Error al obtener la información del producto:", e)
    finally:
        if conn:
            conn.close()

#Obtener historial de ventas
def obtener_registro_ventas():
    try:
        conn = connection()
        cursor = conn.cursor()
        # Consulta para obtener el registro de ventas con el monto total
        query = """
        SELECT v.id, v.producto, v.cantidad, p.precio, (v.cantidad * p.precio) AS monto_total
        FROM ventas v
        JOIN productos p ON v.producto = p.nombre;
        """
        cursor.execute(query)
        ventas = cursor.fetchall()
        
        if ventas:
            print("Registro de ventas:")
            for venta in ventas:
                id_venta, producto, cantidad, precio, monto_total = venta
                print(f"ID Venta: {id_venta}, Producto: {producto}, Cantidad: {cantidad}, Precio: {precio}, Monto Total: {monto_total}")
        else:
            print("No hay ventas registradas.")
        
    except psycopg2.Error as e:
        print("Error al obtener el registro de ventas:", e)
    finally:
        if conn:
            conn.close()

#Obtener los productos con un bajo stock
def obtener_producto_bajo_stock():
    try:
        conn = connection()
        cursor = conn.cursor()

        # Consulta para obtener la información del producto
        query = "SELECT nombre, descripcion, precio, cantidad_stock FROM productos WHERE cantidad_stock < 10"
        cursor.execute(query)
        productos = cursor.fetchall()
        
        
        if productos:
            for producto in productos: 
                nombre, descripcion, precio, cantidad_stock = producto
                print(f"Nombre: {nombre}")
                print(f"Descripción: {descripcion}")
                print(f"Precio: {precio}")
                print(f"Cantidad en stock: {cantidad_stock}")
        else:
            print("Producto no encontrado.")

    except psycopg2.Error as e:
        print("Error al obtener la información del producto:", e)
    finally:
        if conn:
            conn.close()

#Actualizar el inventario
def actualizar_inventario():
    try:
        conn = connection()
        cursor = conn.cursor()

        # Solicitar el nombre del producto a actualizar
        producto = input("Ingrese el nombre del producto a actualizar: ")

        # Verificar si el producto existe en la base de datos
        select_query = "SELECT nombre, cantidad_stock, precio FROM productos WHERE nombre = %s"
        cursor.execute(select_query, (producto,))
        producto_info = cursor.fetchone()

        if producto_info:
            print(f"Producto encontrado: {producto_info[0]}")
            print(f"Cantidad actual en stock: {producto_info[1]}")
            print(f"Precio actual: {producto_info[2]}")

            # Solicitar al administrador qué desea actualizar
            opcion = input("¿Qué desea actualizar? (1: Cantidad en stock, 2: Precio): ")

            if opcion == "1":
                nueva_cantidad = int(input("Ingrese la nueva cantidad en stock: "))
                update_query = "UPDATE productos SET cantidad_stock = %s WHERE nombre = %s"
                cursor.execute(update_query, (nueva_cantidad, producto))
                conn.commit()
                print("Cantidad en stock actualizada exitosamente.")
            elif opcion == "2":
                nuevo_precio = float(input("Ingrese el nuevo precio: "))
                update_query = "UPDATE productos SET precio = %s WHERE nombre = %s"
                cursor.execute(update_query, (nuevo_precio, producto))
                conn.commit()
                print("Precio actualizado exitosamente.")
            else:
                print("Opción no válida.")
        else:
            print("Producto no encontrado.")

    except psycopg2.Error as e:
        print("Error al actualizar inventario:", e)
    finally:
        if conn:
            conn.close()

#Menu administrador
def menu_administrador():
    print("Menu administrador:")
    print("1. Registrar nuevo producto")
    print("2. Ver información de un producto")
    print("3. Actualizar inventario")
    print("4. Ver informe de productos bajos en stock")
    print("5. Registrar una venta")
    print("6. Ver historial de ventas")
    print("7. Salir")
    opcion = input("Seleccione una opcion: ")

    while(opcion != "7"):
        if opcion == "1":
            registrar_producto()

        elif opcion == "2":
            ver_info_producto()
            
        elif opcion == "3":
            actualizar_inventario()

        elif opcion == "4":
            obtener_producto_bajo_stock()

        elif opcion == "5":
            producto = input("Ingrese el nombre del producto: ")
            cant = input("Ingrese la cantidad a comprar: ")
            if not cant.isdigit():
                print("Ingrese una cantidad válida")
                continue
            cantidad = int(cant)
            registrar_venta(producto, cantidad)  # Cliente será NULL

        elif opcion == "6":
            obtener_registro_ventas()

        else:
            print("Ingrese una opcion valida")

        opcion = input("Seleccione una opcion: ")

#Ver informacion personal del cliente
def ver_informacion_personal(user):
    try:
        username = user[0]
        conn = connection()
        cursor = conn.cursor()

        # Consulta para obtener la información personal del cliente
        select_query = "SELECT nombre, email, direccion FROM clientes WHERE username = %s"
        cursor.execute(select_query, (username,))
        cliente_info = cursor.fetchone()

        if cliente_info:
            print(f"Nombre: {cliente_info[0]}")
            print(f"Email: {cliente_info[1]}")
            print(f"Dirección: {cliente_info[2]}")
        else:
            print("No se encontró información del cliente.")

    except psycopg2.Error as e:
        print("Error al obtener la información personal:", e)
    finally:
        if conn:
            conn.close()

#Ver todos los productos
def ver_catalogo_productos():
    try:
        conn = connection()
        cursor = conn.cursor()

        # Mostrar todos los productos disponibles
        select_query = "SELECT nombre, descripcion, precio, cantidad_stock FROM productos"
        cursor.execute(select_query)
        productos = cursor.fetchall()
        print("Catálogo de productos:")
        for producto in productos:
            print(f"Nombre: {producto[0]}, Descripción: {producto[1]}, Precio: {producto[2]}, Cantidad en stock: {producto[3]}")

    except psycopg2.Error as e:
        print("Error al realizar la compra:", e)
    finally:
        if conn:
            conn.close()

#Cliente realiza una compra
def realizar_compra(user):
    try:
        conn = connection()
        cursor = conn.cursor()

        while True:
            producto = input("Ingrese el nombre del producto que desea comprar (o 'salir' para terminar): ")
            if producto.lower() == 'salir':
                break

            cant = input("Ingrese la cantidad que desea comprar: ")
            if not cant.isdigit():
                print("Por favor, ingrese un número válido para la cantidad.")
                continue

            cantidad = int(cant)
            registrar_venta(producto, cantidad, user[0])

    except psycopg2.Error as e:
        print("Error al realizar la compra:", e)
    finally:
        if conn:
            conn.close()

#Menu cliente
def menu_cliente(user):
    print("Menu cliente:")
    print("1. Ver información personal")
    print("2. Ver catálogo de productos")
    print("3. Realizar una compra")
    print("4. Salir del sistema")
    opcion = input("Seleccione una opcion: ")

    while(opcion != "4"):
        if opcion == "1":
            ver_informacion_personal(user)

        elif opcion == "2":
            ver_catalogo_productos()
            
        elif opcion == "3":
            realizar_compra(user)

        else:
            print("Ingrese una opcion valida")

        print("Menu cliente:")
        print("1. Ver información personal")
        print("2. Ver catálogo de productos")
        print("3. Realizar una compra")
        print("4. Salir del sistema")
        opcion = input("Seleccione una opcion: ")

#Inicio de sesion
def login():
    username = input("Ingrese su nombre de usuario: ")
    password = input("Ingrese su contraseña: ")
    try:
        conn = connection()
        select_query = "SELECT * FROM usuarios WHERE username = %s"
        cursor = conn.cursor()
        cursor.execute(select_query, (username,))
        user = cursor.fetchone()
        if user:
            if user[1] == password:
                # Verificar el rol del usuario
                if user[2] == "administrador":
                    print("Bienvenido administrador.")
                    menu_administrador()
                elif user[2] == "cliente":
                    print("Bienvenido cliente.")
                    menu_cliente(user)
            else:
                    # Contraseña incorrecta
                    print("Contraseña incorrecta. Por favor, intente nuevamente.")
                    login()
        else:
            print("Usuario no existe. Por favor, regístrese.")
            register_new_user()
            login()
    except psycopg2.Error as e:
        print("Error al iniciar sesión:", e)
    finally:
        if conn:
            conn.close()

if connection():
    login()
