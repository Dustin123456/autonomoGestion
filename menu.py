import tareas
import restauracion
import reporte

def menu():
    print("\n Menu")
    print("1. Añadir usuario")
    print("2. Actualizar usuario")
    print("3. Eliminar usuario")
    print("4. Añadir rol")
    print("5. Asignar rol a usuario")
    print("6. Obtener usuarios")
    print("7. Obetener roles")
    print("8. Respaldar base de datos")
    print("9. Restaurar base de datos")
    print("10. Generar reporte")
    print("11. Generar procedimientos almacenados")
    print("12. Salir")

def main():
    while True:
        menu()
        pick = input("Selecciona una opción: ")

        if pick == '1':
            tareas.addUser()
        elif pick == '2':
            tareas.updateUser()
        elif pick == '3':
            tareas.deleteUser()
        elif pick == '4':
            print("4")
        elif pick == '5':
            print("5")
        elif pick == '6':
            tareas.getUsers()
        elif pick == '7':
            tareas.getRoles()
        elif pick == '8':
            restauracion.respaldo()
        elif pick == '9':
            restauracion.restaurar()
        elif pick == '10':
            reporte.generar()
        elif pick == '11':
            tareas.procedimientosAlmacenados()
        elif pick == '12':
            tareas.cerrarMenu()
            break
        else:
            print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    main()
