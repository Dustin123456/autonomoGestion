import mysql.connector


conexion = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456'
)

HOST = 'localhost'


def addUser():
    try:
        usuario = input("Ingresa el nombre del usuario: ")
        contraseña = input("Ingresa la contraseña: ")
        
        cursor = conexion.cursor()
        sql = f"CREATE USER '{usuario}'@'{HOST}' IDENTIFIED BY '{contraseña}'"
        cursor.execute(sql)

        conexion.commit()
        print("Usuario agredado correctamente.")
    
    except mysql.connector.Error as error:
        print("Error al agregar usuario:", error)

    finally:
        cursor.close()
        print("Cursor cerrado.")



def updateUser():
    try:
        usuario = input("Ingresa el nombre del usuario que quiere actualizar: ")
        nuevoUsuario = input("Ingresa el nuevo nombre del usuario: ")
        
        contraseña = input("Ingresa la nueva contraseña: ")
        cursor = conexion.cursor()
        
        sql = f"RENAME USER '{usuario}'@'{HOST}' TO '{nuevoUsuario}'@'{HOST}'"
        cursor.execute(sql)
        conexion.commit()
        
        sql2 = f"ALTER USER '{nuevoUsuario}'@'{HOST}' IDENTIFIED BY '{contraseña}'"
        cursor.execute(sql2)
        conexion.commit()
        
        print("Usuario modificado correctamente.")
    
    except mysql.connector.Error as error:
        print("Error al modificar usuario:", error)

    finally:
        cursor.close()
        print("Cursor cerrado.")


def deleteUser():
    try: 
        usuario = input("Ingresa el nombre del usuario que quiere eliminar: ")
        cursor = conexion.cursor()
        sql = f"DROP USER '{usuario}'@'{HOST}'"
        cursor.execute(sql)
        
        conexion.commit()
        print("Usuario eliminado correctamente.")
    
    except mysql.connector.Error as error:
        print("Error al eliminar usuario:", error)

    finally:
        cursor.close()
        print("Cursor cerrado.")


def getUsers():
    try:
        cursor = conexion.cursor()
        sql = f"SELECT user FROM mysql.user"
        cursor.execute(sql)
        resultados = cursor.fetchall()

        for fila in resultados:
            print(fila)
        print("Presione enter para continuar")
        input()

    
    except mysql.connector.Error as error:
        print("Error al obtener usuarios:", error)

    finally:
        cursor.close()
        print("Cursor cerrado.")



def getRoles():
    try:
        cursor = conexion.cursor()
        sql = f"""SELECT COLUMN_NAME
                    FROM information_schema.COLUMNS
                    WHERE TABLE_NAME = 'user' 
                    AND TABLE_SCHEMA = 'mysql' 
                    AND COLUMN_TYPE LIKE "enum('N','Y')"
                    AND IS_NULLABLE = 'NO'"""

        cursor.execute(sql)
        resultados = cursor.fetchall()

        for fila in resultados:
            print(fila)
        print("Presione enter para continuar")
        input()
    
    except mysql.connector.Error as error:
        print("Error al obtener privilegios:", error)

    finally:
        cursor.close()
        print("Cursor cerrado.")


def procedimientosAlmacenados():
    conexion = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456',
        database='kinder_db'
    )
    try:
        cursor = conexion.cursor()
        cursor.execute("SHOW TABLES FROM kinder_db")
        tablas = cursor.fetchall()

        with open('procedimientos_almacenados.sql', 'w') as archivo:
            archivo.write(f"DELIMITER $$\n\n")
            
            for tabla in tablas:
                nombre_tabla = tabla[0]
                cursor.execute(f"DESCRIBE {nombre_tabla}")
                columnas = cursor.fetchall()
                
                primary_key = None
                columnas_nombres = []
                columnas_parametros = []
                columnas_update = []
                
                for columna in columnas:
                    col_name = columna[0]
                    col_type = columna[1]
                    if columna[3] == 'PRI' and columna[5] == 'auto_increment':
                        primary_key = col_name
                    else:
                        columnas_nombres.append(col_name)
                        columnas_parametros.append(f"IN p_{col_name} {col_type}")
                        columnas_update.append(f"{col_name} = p_{col_name}")

                columnas_insert = ", ".join(columnas_nombres)
                columnas_parametros = ", ".join(columnas_parametros)
                
                archivo.write(f"CREATE PROCEDURE Insertar_{nombre_tabla} ({columnas_parametros}) \n")
                archivo.write(f"BEGIN\n")
                archivo.write(f"    INSERT INTO {nombre_tabla} ({columnas_insert}) VALUES ({', '.join([f'p_{col}' for col in columnas_nombres])});\n")
                archivo.write(f"END $$\n\n")
                
                if primary_key:
                    archivo.write(f"CREATE PROCEDURE Actualizar_{nombre_tabla} (IN p_{primary_key} {columnas[0][1]}, {columnas_parametros}) \n")
                    archivo.write(f"BEGIN\n")
                    archivo.write(f"    UPDATE {nombre_tabla} SET {', '.join(columnas_update)} WHERE {primary_key} = p_{primary_key};\n")
                    archivo.write(f"END $$\n\n")
                
                if primary_key:
                    archivo.write(f"CREATE PROCEDURE Eliminar_{nombre_tabla} (IN p_{primary_key} {columnas[0][1]}) \n")
                    archivo.write(f"BEGIN\n")
                    archivo.write(f"    DELETE FROM {nombre_tabla} WHERE {primary_key} = p_{primary_key};\n")
                    archivo.write(f"END $$\n\n")
                
                archivo.write(f"CREATE PROCEDURE ObtenerTodos_{nombre_tabla} () \n")
                archivo.write(f"BEGIN\n")
                archivo.write(f"    SELECT * FROM {nombre_tabla};\n")
                archivo.write(f"END $$\n\n")
            
            archivo.write(f"DELIMITER ;\n")
    
        print("Scripts de procedimientos almacenados generados correctamente.")
    
    except mysql.connector.Error as error:
        print("Error al generar script: ", error)

    finally:
        cursor.close()
        print("Cursor cerrado.")
        print("Presione enter para regresar al menú..")
        input()


def cerrarMenu():
    print(conexion.is_connected())
    if conexion.is_connected():
        conexion.close()
        print("Conexión cerrada.")
        print("Hasta luego.")
    else: 
        print("Saliendo del gestor.")