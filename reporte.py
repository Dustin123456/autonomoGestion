import mysql.connector
from fpdf import FPDF

conexion = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456'
)

def generar(): 
    try: 
        cursor = conexion.cursor()
        sql = f"""SELECT TABLE_NAME
                    FROM information_schema.TABLES
                    WHERE TABLE_SCHEMA = 'kinder_db'"""
                    
        cursor.execute(sql)
        
        resultados = cursor.fetchall()
        for fila in resultados:
            print(fila)
        table = input("Ingresa la entidad con la quiere generar un reporte: ")
        atributos(table)
    except mysql.connector.Error as error:
        print("Error al listar entidades:", error)

def atributos(table):
    try: 
        cursor = conexion.cursor()
        sql = f"""SELECT COLUMN_NAME
                        FROM information_schema.COLUMNS
                        WHERE TABLE_NAME = '{table}' 
                        AND TABLE_SCHEMA = 'kinder_db'"""
        
        cursor.execute(sql)
        resultados = cursor.fetchall()
        for fila in resultados:
            print(fila)
        reporte(table)

    except mysql.connector.Error as error:
        print("Error al listar atributos:", error)            

def reporte(table):
    try: 
        cursor = conexion.cursor()
        columnas = input('Ingrese las columnas con las que quiere generar un reporte(separe los atributos con una ","): ')

        sql = f"""SELECT {columnas}
                        FROM kinder_db.{table}"""
        cursor.execute(sql)
        
        resultados = cursor.fetchall()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        reporteNombre = input("Ingrese el nombre de su reporte: ")

        pdf.cell(180, 10, txt="Reporte", border=1, ln=True, align='C')
        header = columnas.split(',')
        for col in header:
            pdf.cell(40, 10, col, border=1)
        pdf.ln()


        for fila in resultados:
            for dato in fila:
                pdf.cell(40, 10, str(dato), border=1)
            pdf.ln()

        pdf.output(f"{reporteNombre}.pdf")
        print("Reporte generado satisfactoriamente.")
        print("Presione enter para regresar al menú..")
        input()
        
    except mysql.connector.Error as error:
        print("Error al generar reporte:", error)

    finally:
        cursor.close()
        print("Cursor cerrado.")