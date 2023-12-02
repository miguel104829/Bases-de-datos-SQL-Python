import mysql.connector
import os
import subprocess
import datetime

#Conexión con la base de datos
acceso_bd = {"host": "localhost",
             "user": "root",
            "password": ""
            }

#Rutas
#Obtenemos la raiz de la carpeta del proyecto
carpeta_principal = os.path.dirname(__file__)

carpeta_respaldo = os.path.join(carpeta_principal, "respaldo")

class BaseDatos:
    def __init__(self, **Kwargs):
        self.conector = mysql.connector.connect(**Kwargs)
        self.cursor = self.conector.cursor()
        self.host = Kwargs["host"]
        self.usuario = Kwargs["user"]
        self.contraseña = Kwargs["password"]
        self.conexion_cerrada = False
        #Avisa que se abrio la conexión con el servidor
        print("Se abrió la conexión con el servidor.")
                
    #Decorador para el reporte de base de datos en el servidor
    def reporte_bd(funcion_parametro):
        def interno(self, nombre_bd):
            funcion_parametro(self, nombre_bd)
            BaseDatos.mostrar_bd(self)
        return interno
    
    #Decorador para el cierre del cursor y la base de datos
    def conexion(funcion_parametro):
        def interno(self, *args, **kwargs):
            try:
                if self.conexion_cerrada:
                    self.conector = mysql.connector.connect(
                        host=self.host,
                        user=self.usuario,
                        password=self.contraseña
                    )
                    self.cursor = self.conector.cursor()
                    self.conexion_cerrada = False
                    print("Se abrió la conexión con el servidor.")
                #se llama a la función externa
                funcion_parametro(self, *args, **kwargs)
            except Exception as e:
                #se informa de un error en la llamada
                print(f"Ocurrió un error: {e}")
                #propagacion de la excepción
                raise e
            finally:
                if self.conexion_cerrada:
                    pass
                else:
                    #cerramos el cursor y la conexión
                    self.cursor.close()
                    self.conector.close()
                    print("Se cerró la conexión con el servidor.")
                    self.conexion_cerrada = True
            return self.resultado
        return interno       
    
    #Decorador para comprobar si existe una base de datos
    def comprueba_bd(funcion_parametro):
        def interno(self, nombre_bd, *args):
            #Primero se verifica si la base de datos existe
            sql = f"SHOW DATABASES LIKE '{nombre_bd}'"
            self.cursor.execute(sql)
            resultado = self.cursor.fetchone()
            #Si no existe, se muestra un mensaje de error y termina el método
            if not resultado:
                print(f"La base de datos {nombre_bd} no existe.")
                return
            #Ejecuta la fucnión decoradora y devuelve el resultado
            return funcion_parametro(self, nombre_bd, *args)
        return interno
    
    #Hacer consultas a la base de datos
    @conexion
    def consulta(self, sql):
        self.cursor.execute(sql)
        self.resultado = self.cursor.fetchall()
       
    #Mostrar las bases de datos
    @conexion
    def mostrar_bd(self):    
        self.cursor.execute("SHOW DATABASES")
        self.resultado = self.cursor.fetchall()
                
    #Elimanar una base de datos
    @conexion
    @reporte_bd
    @comprueba_bd
    def eliminar_bd(self, nombre_bd):
        self.cursor.execute(f"DROP DATABASE {nombre_bd}")
        print(f"Base de datos {nombre_bd} eliminada.")
                
    #Crear una base de datos
    @conexion
    @reporte_bd
    def crear_bd(self, nombre_bd):
        try:
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {nombre_bd}")
            print(f"Se creo la base de datos {nombre_bd} o ya estaba creada.")
        except:
            print(f"Ocurrió un error al intentar crear la base de datos {nombre_bd}.")
    
    #Crear backup de bases de datos
    @conexion
    @comprueba_bd
    def copia_bd(self, nombre_bd):
               
        #obtiene la fecha y hora actual
        self.fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        with open(f'{carpeta_respaldo}/{nombre_bd}_{self.fecha_hora}.sql', 'w') as out:
                subprocess.Popen(f'"C:/Program Files/MySQL/MySQL Server 8.0/bin/mysqldump" --user=root --password={self.contraseña} --databases {nombre_bd}', stdout=out, shell=True)
        print(f"Se creo la copia de la base de datos {nombre_bd}.")       
            
       
    @conexion
    @comprueba_bd
    def crear_tabla(self, nombre_bd, nombre_tabla, columnas):
        try:
            #String para guardar el string de las columnas y tipos de datos
            columnas_str = ""
            #Se itera la lista que se le pasa como argumento (cada diccionario)
            for columna in columnas:
                #formamos el string con nombre,, tipo y longitud
                columnas_str += f"{columna['nombre']} {columna['tipo']}({columna['longitud']})"
                #Si es clave primaria, autoincrementable y no nulo se agrega al string
                if columna['primary_key']:
                    columnas_str += " PRIMARY KEY"
                if columna['auto_increment']:
                    columnas_str += " AUTO_INCREMENT"
                if columna['null']:
                    columnas_str += " NOT NULL"
                #Hace un salto de linea despues de cada diccionario
                columnas_str += ",\n"
            #Elimina al final el salto de linea y la coma
            columnas_str = columnas_str[:-2]
            #le indica que base de datos va a usar
            self.cursor.execute(f"USE {nombre_bd}")
            #se crea la tabla juntando la instrucción SQL con el string generado
            sql = f'CREATE TABLE {nombre_tabla} ({columnas_str});'
            #se ejecuta la instrucción
            self.cursor.execute(sql)
            #se hace efectiva
            self.conector.commit()
            print(f"Se creo la tabla {nombre_tabla} en la base de datos {nombre_bd}.")
        except:
            print(f"Ocurrió un error al intentar crear la tabla {nombre_tabla}.")
    
    @conexion
    @comprueba_bd
    def eliminar_tabla(self, nombre_bd, nombre_tabla):
        try:
            self.cursor.execute(f"USE {nombre_bd}")
            self.cursor.execute(f"DROP TABLE {nombre_tabla}")
            print(f"Se elimino la tabla {nombre_tabla} de la base de datos {nombre_bd}.")
        except:
            print(f"Ocurrió un error al intentar eliminar la tabla {nombre_tabla}.")
            
    @conexion
    @comprueba_bd
    def mostrar_tablas(self, nombre_bd):
        #Se selecciona la base de datos
        self.cursor.execute(f"USE {nombre_bd}")
        #Se informa que se van a mostrar las tablas
        print(f"Estas son las tablas de la base de datos {nombre_bd}:")
        #Realiza la consulta para mostrar las tablas
        self.cursor.execute("SHOW TABLES")
        resultado = self.cursor.fetchall()
        #Evalua si no hay tablas en la base de datos
        if resultado == []:
            print(f"No hay tablas en la base de datos {nombre_bd}.")
            return
        #Recorre el resultado y muestra por pantalla
        for tabla in resultado:
            print(f'-> {tabla[0]}.')                   
        
            
    @conexion
    @comprueba_bd
    def mostrar_columnas(self, nombre_bd, nombre_tabla):
        #Establece la base de datos actual
        self.cursor.execute(f"USE {nombre_bd}")
        try:
            #Realizar la consulta para mostrar las columnas de la tabla
            self.cursor.execute(f"SHOW COLUMNS FROM {nombre_tabla}")
            resultado = self.cursor.fetchall()
            
            #Se informa que se van a mostrar las columnas
            print(f"Estas son las columnas de la tabla {nombre_tabla}:")
            #Recorre los resultados y los muestra por pantalla
            for columna in resultado:
                not_null = "No admite valores nulos." if columna[2] == "NO" else ""
                primary_key = "Es clave primaria." if columna[3] == "PRI" else ""
                foreing_key = "Es clave externa." if columna[3] == "MUL" else ""
                print(f'-> {columna[0]} ({columna[1]}) {not_null} {primary_key} {foreing_key}')
        except:
            print(f"Ocurrió un error. Comprueba el nombre de la tabla.") 
        
    @conexion
    def insertar_registro(self, nombre_bd, nombre_tabla, registro):
        self.cursor.execute(f"USE {nombre_bd}")
        
        if not registro:
            print("La lista de registro está vacía.")
            return
    
        #obtener las columnas y los valores de cada diccionario
        columnas = []
        valores = []
        for registro in registro:
            columnas.extend(registro.keys())
            valores.extend(registro.values())
        
        #convertir las columnas y valores a string
        columnas_str = ""
        for columna in columnas:
            columnas_str += f"{columna}, "
        columnas_str = columnas_str[:-2] #Quitar la última coma y el espacio
        
        valores_str = ""
        for valor in valores:
            valores_str += f"'{valor}', "
        valores_str = valores_str[:-2]
        
        #crear la instrucción de insercción
        sql = f"INSERT INTO {nombre_tabla} ({columnas_str}) VALUES ({valores_str})"
        self.cursor.execute(sql)
        self.conector.commit()
        print(f"Se insertó el registro en la tabla {nombre_tabla} de la base de datos {nombre_bd}.")
    
    #Eliminar registros con una condición
    @conexion
    @comprueba_bd
    def eliminar_registro(self, nombre_bd, nombre_tabla, condicion):
        self.cursor.execute(f"USE {nombre_bd}")
        try:
            #se selecciona la base de datos
            self.cursor.execute(f"USE {nombre_bd}")
            #se crea la instrucción de eliminación
            sql = f"DELETE FROM {nombre_tabla} WHERE {condicion}"
            self.cursor.execute(sql)
            self.conector.commit()
            print(f"Se eliminaron los registros de la tabla {nombre_tabla} de la base de datos {nombre_bd}.")
        except:
            print(f"Ocurrió un error al intentar borrar registros en la tabla.")
        
    #Eliminar todos los registros de una tabla
    @conexion
    @comprueba_bd
    def vaciar_tabla(self, nombre_bd, nombre_tabla):
        try:
            #se selecciona la base de datos
            self.cursor.execute(f"USE {nombre_bd}")
            #se borran todos los registros de una tabla
            sql = f"TRUNCATE TABLE {nombre_tabla}"
            self.cursor.execute(sql)
            self.conector.commit()
            print(f"Se han borrado todos los registros de la tabla {nombre_tabla} de la base de datos {nombre_bd}.")
        except:
            print(f"Ocurrió un error al intentar borrar registros de la tabla.")
    
    #Actualizar registros de una tabla
    @conexion
    @comprueba_bd
    def actualizar_registro(self, nombre_bd, nombre_tabla, columnas, condiciones):
        try:
            #se selecciona la base de datos
            self.cursor.execute(f"USE {nombre_bd}")
            #se crea la instrucción de actualización
            sql = f"UPDATE {nombre_tabla} SET {columnas} WHERE {condiciones}"
            self.cursor.execute(sql)
            self.conector.commit()
            print(f"Se actualizó el registro de la tabla {nombre_tabla} de la base de datos {nombre_bd}.")
        except:
            print(f"Ocurrió un error al intentar actualizar el registro de la tabla.")
             
