#import bd.base_datos as sqlbd
#import bd.tablas as tbl 
import interfaz.interfaz_grafica as gui

#ase_datos = sqlbd.BaseDatos(**sqlbd.acceso_bd)b

# registro = [{"nombre": "Juan",
#              "apellido": "Perez",
#              "telefono": "786959404",
#              "direccion": "C/cualquiera"    
# }]

#base_datos.eliminar_registro("pruebas", "usuarios", "nombre = 'Juan'")
#base_datos.insertar_registro("pruebas", "usuarios", registro)
#base_datos.mostrar_bd()
#base_datos.eliminar_bd("pruebas")
#base_datos.eliminar_bd("pruebas2")
#base_datos.consulta("SHOW DATABASES")
#base_datos.consulta("SHOW DATABASES")
#base_datos.crear_tabla("pruebas", "usuarios", tbl.columnas)
#base_datos.eliminar_tabla("pruebas", "usuarios")
#base_datos.crear_bd("pruebas")
#base_datos.copia_bd("world")
#base_datos.mostrar_tablas("pruebas")
#base_datos.mostrar_columnas("world", "cityasd") 
#base_datos.vaciar_tabla("pruebas", "usuarios")
#base_datos.actualizar_registro("pruebas", "usuarios", "nombre = 'Juanito'", "nombre = 'Juan'")

#ventana_opciones = gui.VentaOpciones()
ventana_login = gui.Login()