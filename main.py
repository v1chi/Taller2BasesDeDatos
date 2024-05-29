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
    finally:
        if conn:
            conn.close()

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
    finally:
        if conn:
            conn.close()

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
    finally:
        if conn:
            conn.close()

# Función para poblar la tabla de usuarios
def poblar_tabla_usuarios():
    usuarios_data = [
        ("camilo@tienda.com", "camilo@7720", "administrador"),
        ("adrian", "poCa12_", "administrador"),
        ("vichi", "guA_34", "administrador"),
        ("carlos.p", "Omg43#", "cliente"),
        ("juannn", "Pa$$w0", "cliente"),
        ("anita", "Abc123!", "cliente"),
        ("pedrito", "Xyz789@", "cliente"),
        ("luisa", "Y0u!r4", "cliente"),
        ("javelo", "H@ppy5", "cliente"),
        ("heu.remi", "uCN_2e", "cliente"),
        ("winteroh", "hawA11_", "cliente"),
        ("camilo.a", "baSe2!", "cliente"),
        ("vixo.r", "Qr$456", "cliente"),
    ]
    try:
        conn = connection()
        cursor = conn.cursor()
        # En caso de encontrar nombres de usuarios duplicados en alguna tupla, no se inserta.
        insert_query = """
        INSERT INTO usuarios (username, password, role) VALUES (%s, %s, %s)
        ON CONFLICT (username) DO NOTHING;
        """
        cursor.executemany(insert_query, usuarios_data)
        conn.commit()
        print("Tabla de usuarios poblada exitosamente.")
    except psycopg2.Error as e:
        print("Error al poblar la tabla de usuarios:", e)
    finally:
        if conn:
            conn.close()

# Función para poblar la tabla de clientes
def poblar_tabla_clientes():
    clientes_data = [
        ("carlos.p", "carlos", "tulipanes 23", "carlitosp@gmail.com"),
        ("juannn", "juan", "rosas 1", "juaninn@gmail.com"),
        ("anita", "ana", "pimientos 2", "anitanita@gmail.com"),
        ("pedrito", "pedro", "pimientos 8", "pedropedropedro@gmail.com"),
        ("luisa", "luisa", "las dalias 42", "gatosss1@gmail.com"),
        ("javelo", "javier", "los platanos 1541", "javelo89@gmail.com"),
        ("heu.remi", "remi", "los copihues 2257", "heuremi03@gmail.com"),
        ("winteroh", "winter", "petunias 33", "invierno2@gmail.com"),
        ("camilo.a", "camilo", "azucenas 21", "camilito@gmail.com"),
        ("vixo.r", "vicente", "las torres 77", "vixovixo@gmail.com"),
    ]

    try:
        conn = connection()
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO clientes (username, nombre, direccion, email) VALUES (%s, %s, %s, %s)
        ON CONFLICT (username) DO NOTHING;
        """
        cursor.executemany(insert_query, clientes_data)
        conn.commit()
        print("Tabla de clientes poblada exitosamente.")
    except psycopg2.Error as e:
        print("Error al poblar la tabla de clientes:", e)
    finally:
        if conn:
            conn.close()

# Función para poblar la tabla de productos
def poblar_tabla_productos():
    productos_data = [
        ("Laptop", "Laptop HP con 16GB RAM", 1200, 15),
        ("Smartphone", "iPhone 12 Pro", 999, 30),
        ("Tablet", "iPad Pro 11 pulgadas", 799, 20),
        ("Monitor", "Monitor Dell 24 pulgadas", 300, 25),
        ("Teclado", "Teclado mecánico Logitech", 120, 50),
        ("Ratón", "Ratón inalámbrico Logitech", 50, 60),
        ("Impresora", "Impresora multifunción HP", 150, 10),
        ("Auriculares", "Auriculares Bluetooth Sony", 200, 40),
        ("Altavoz", "Altavoz portátil JBL", 100, 35),
        ("Cámara", "Cámara digital Canon", 500, 8),
        ("Microondas", "Microondas Samsung", 150, 20),
        ("Refrigerador", "Refrigerador LG", 800, 5),
        ("Lavadora", "Lavadora Samsung", 600, 10),
        ("Televisor", "Televisor Sony 50 pulgadas", 900, 7),
        ("Consola", "Consola PlayStation 5", 499, 25),
        ("Juego", "Videojuego FIFA 23", 60, 100),
        ("Router", "Router WiFi TP-Link", 80, 45),
        ("SSD", "Disco SSD Samsung 1TB", 150, 70),
        ("Memoria RAM", "Memoria RAM Kingston 8GB", 40, 80),
        ("Disco Duro", "Disco duro externo Seagate 2TB", 100, 55),
    ]

    try:
        conn = connection()
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO productos (nombre, descripcion, precio, cantidad_stock) VALUES (%s, %s, %s, %s)
        ON CONFLICT (nombre) DO NOTHING;
        """
        cursor.executemany(insert_query, productos_data)
        conn.commit()
        print("Tabla de productos poblada exitosamente.")
    except psycopg2.Error as e:
        print("Error al poblar la tabla de productos:", e)
    finally:
        if conn:
            conn.close()

# Función para poblar la tabla de ventas
def poblar_tabla_ventas():
    ventas_data = [
        (1, "carlos.p", "Laptop", 1),
        (2, "juannn", "Smartphone", 2),
        (3, "anita", "Tablet", 1),
        (4, "javelo", "Monitor", 1),
        (5, "javelo", "Teclado", 2),
        (6, "winteroh", "Ratón", 3),
        (7, "heu.remi", "Impresora", 1),
        (8, "javelo", "Auriculares", 2),
    ]

    try:
        conn = connection()
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO ventas (id, cliente, producto, cantidad) VALUES (%s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
        """
        cursor.executemany(insert_query, ventas_data)
        conn.commit()
        print("Tabla de ventas poblada exitosamente.")
    except psycopg2.Error as e:
        print("Error al poblar la tabla de ventas:", e)
    finally:
        if conn:
            conn.close()

#Funcion para verificar si la contraseña es válida
def is_valid_password(password):
    # La contraseña debe tener entre 6 y 8 caracteres
    if len(password) < 6 or len(password) > 8:
        return False
    # Al menos una letra mayúscula
    if not re.search("[A-Z]", password):
        return False
    # Al menos un número 
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
        #Si la contraseña no es válida, se indica que hubo un error
        if not is_valid_password(password):
            print("La contraseña no cumple con los requisitos.")
            return
        #Si el rol no es cliente o administrador, se indica que no es valido
        if role != "cliente" and role != "administrador":
            print("El rol no es valido")
            return

        #Si la contraseña y el rol son validos, se crea el usuario
        insert_query = "INSERT INTO usuarios (username, password, role) VALUES (%s, %s, %s)"
        conn = connection()
        cursor = conn.cursor()
        cursor.execute(insert_query, (username, password, role))
        conn.commit()
        print("Usuario registrado exitosamente.")

        #Además, si el usuario es de tipo cliente, se pide su nombre y sus datos de contacto (email y direccion) y se registra como cliente
        if role == "cliente":
            nombre = input("Ingrese su nombre: ")
            email = input("Ingrese su email: ")
            direccion = input("Ingrese su dirección: ")
            register_client(username, email, direccion, nombre)
    except psycopg2.Error as e:
        print("Error al registrar usuario:", e) 

#Registrar un nuevo producto
def registrar_producto():
    #Se pide el nombre, descripcion, precio y cantidad de stock del producto
    nombre = input("Ingrese el nombre del producto: ")
    descripcion = input("Ingrese la descripcion del producto: ")
    precio = input("Ingrese el precio del producto: ")
    cantidad_stock = input("Ingrese la cantidad de stock del producto: ")

    try:
        #Si el precio no es un numero o si la cantidad de stock no es un numero, se indica que hubo un error
        if not precio.isdigit() and not cantidad_stock.isdigit():
            print("Ingrese valores correctos para el precio y el stock (tienen que ser numeros enteros)")
            return
        #Si el precio y stock estan bien, se ingresa el producto
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
    #Se selecciona el maximo id de venta y se le suma 1
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM ventas;")
    ultimo_id = cursor.fetchone()[0]
    conn.close()
    #Si es la primera venta, se retorna 0
    return ultimo_id if ultimo_id is not None else 0

#Registrar una venta
def registrar_venta(producto, cantidad, cliente):
    try:
        # Buscar el producto y sacar su cantidad de stock
        select_query = "SELECT cantidad_stock FROM productos WHERE nombre = %s"
        conn = connection()
        cursor = conn.cursor()
        cursor.execute(select_query, (producto,))
        cantidad_stock = cursor.fetchone()

        #Se verifica si la cantida de stock es no nula y si hay suficiente stock del producto
        if cantidad_stock and cantidad_stock[0] >= cantidad:

            # Restar la cantidad vendida del stock del producto
            update_query = "UPDATE productos SET cantidad_stock = cantidad_stock - %s WHERE nombre = %s"
            cursor.execute(update_query, (cantidad, producto))
            nuevo_id = obtener_ultimo_id() + 1 #Crear id de la venta
            
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

        #Se verifica si el producto es no nulo
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
        # Consulta para obtener el registro de ventas, calculando el monto total
        query = """
        SELECT v.id, v.cliente, v.producto, v.cantidad, p.precio, (v.cantidad * p.precio) AS monto_total
        FROM ventas v
        JOIN productos p ON v.producto = p.nombre;
        """
        cursor.execute(query)
        ventas = cursor.fetchall()
        
        #Se verifica si se encontraron ventas
        if ventas:
            print("Registro de ventas:")
            #Se obtiene la info de cada venta
            for venta in ventas:
                id_venta, cliente, producto, cantidad, precio, monto_total = venta
                print(f"ID Venta: {id_venta}, Nombre cliente: {cliente}, Producto: {producto}, Cantidad: {cantidad}, Precio: {precio}, Monto Total: {monto_total}")
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
        #En esta caso el umbral seleccionado fue de 10, es decir los prooductos con menos de 10 unidades en stock se consideran en bajo stock
        query = "SELECT nombre, descripcion, precio, cantidad_stock FROM productos WHERE cantidad_stock < 10"
        cursor.execute(query)
        productos = cursor.fetchall()
        
        #Se verifica si se encontraron productos en bajo stock
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

            # Modificar cantidad en stock
            if opcion == "1":
                cantidad = input("Ingrese la nueva cantidad en stock: ")
                #Se verifica si la cantidad es un numero
                if not cantidad.isdigit():
                    print("Ingrese una cantidad valida")
                    return
                nueva_cantidad = int(cantidad)
                #Se actualiza el stock
                update_query = "UPDATE productos SET cantidad_stock = %s WHERE nombre = %s"
                cursor.execute(update_query, (nueva_cantidad, producto))
                conn.commit()
                print("Cantidad en stock actualizada exitosamente.")

            #Modificar el precio
            elif opcion == "2":
                precio = input("Ingrese el nuevo precio: ")
                #Se verifica si el precio es un numero
                if not precio.isdigit():
                    print("Ingrese un precio valido")
                    return
                nuevo_precio = int (nuevo_precio)
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

#Cliente realiza una compra
def realizar_compra(user):
    try:
        #Preguntar la cantidad de productos que desea comprar y verificar que sea un valor valido
        cantidad_productos = input("Ingrese la cantidad de productos distintos que desea comprar: ")
        if not cantidad_productos.isdigit():
            print("Por favor, ingrese un número válido para la cantidad de productos distintos.")
            return
        cantidad_productos = int(cantidad_productos)

        #Preguntar por cada producto y cuanto de stock va a comprar
        for i in range(cantidad_productos):
            producto = input("Ingrese el nombre del producto que desea comprar: ")
            cant = input("Ingrese la cantidad que desea comprar: ")
            
            #Se verifica si la cantidad es un numero mayor a 0
            if not cant.isdigit() or (cant.isdigit() and int(cant) <= 0):
                print("Por favor, ingrese un número válido para la cantidad.")
                return

            cantidad = int(cant)
            registrar_venta(producto, cantidad, user[0])

    except psycopg2.Error as e:
        print("Error al realizar la compra:", e)

#Obtener cliente
def obtener_cliente():
    try:
        cliente = input("Ingrese el nombre de usuario del cliente: ")
        select_query_usuario = "SELECT username FROM usuarios WHERE username = %s"
        conn = connection()
        cursor = conn.cursor()
        cursor.execute(select_query_usuario, (cliente,))
        cliente = cursor.fetchone()
        return cliente
     
    except psycopg2.Error as e:
        print("Error al obtener el registro de ventas:", e)
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
            nombre_cliente = obtener_cliente()
            if not nombre_cliente:
                print("El usuario no fue encontrado")
                continue
            realizar_compra(nombre_cliente)

        elif opcion == "6":
            obtener_registro_ventas()

        else:
            print("Ingrese una opcion valida")

        print("Menu administrador:")
        print("1. Registrar nuevo producto")
        print("2. Ver información de un producto")
        print("3. Actualizar inventario")
        print("4. Ver informe de productos bajos en stock")
        print("5. Registrar una venta")
        print("6. Ver historial de ventas")
        print("7. Salir")
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
    #La primera vez que se ejecute el código, se deben quitar las comillas "" para crear las tablas y poblarlas, luego se deben volver a comentar
    """
    #Crear tablas:
    create_users_table()
    create_clientes_table()
    create_products_table()
    create_ventas_table()

    #Poblar tablas:
    poblar_tabla_usuarios()
    poblar_tabla_clientes()
    poblar_tabla_productos()
    poblar_tabla_ventas()
    """
    login()
