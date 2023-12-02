import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import tkinter as tk
import os
from PIL import Image
import bd.base_datos as sqlbd

#Configuraciones globales para la aplicación

# --> Rutas
# Carpeta principal
carpeta_principal = os.path.dirname(__file__)

carpeta_imagenes = os.path.join(carpeta_principal, "imagenes")

#objeto para manejar base de datos MySQL
base_datos = sqlbd.BaseDatos(**sqlbd.acceso_bd)

#Modo de color y tema
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

#Fuentes del programa
fuentes_widgets = ("Raleway", 16, tk.font.BOLD)

class Login:
    def __init__(self):
        # --> Ventana
        self.root = ctk.CTk()
        self.root.title("Login - Proyecto Bases de Datos")
        self.root.iconbitmap(os.path.join(carpeta_imagenes, "1.ico"))
        self.root.geometry("400x550")
        self.root.resizable(False, False)
        
        #contenido de la ventana principal
        #logo
        logo = ctk.CTkImage(
            light_image= Image.open((os.path.join(carpeta_imagenes, "2.jpg"))),
            dark_image= Image.open((os.path.join(carpeta_imagenes, "2.jpg"))),
            size=(300, 300))
        
        #Etiqueta para mostrar la imagen
        etiqueta = ctk.CTkLabel(master = self.root, image=logo, text="")
        etiqueta.pack(pady=15)
               
        #campos de texto
        #usuario
        ctk.CTkLabel(self.root, text="Usuario: ").pack()
        self.usuario = ctk.CTkEntry(self.root)
        self.usuario.insert(0, "Ej: Miguel")
        self.usuario.bind("<Button-1>", lambda e: self.usuario.delete(0, 'end'))
        self.usuario.pack()
        
        #contraseña
        ctk.CTkLabel(self.root, text="Contraseña: ").pack()
        self.contraseña = ctk.CTkEntry(self.root)
        self.contraseña.insert(0, "*"*7)
        self.contraseña.bind("<Button-1>", lambda e: self.contraseña.delete(0, 'end'))
        self.contraseña.pack()
        
        #boton de envío
        ctk.CTkButton(self.root, text="Ingresar", command=self.validar_login).pack(pady=10)
        
        #Bucle de ejecución
        self.root.mainloop()
    
    #funcion para validar el login
    def validar_login(self):
        obtener_usuario = self.usuario.get()
        obtener_contraseña = self.contraseña.get()
        if obtener_usuario == sqlbd.acceso_bd["user"] or obtener_contraseña == sqlbd.acceso_bd["password"]:
            if hasattr(self, "info_login"):
               self.info_login.configure(text="Usuario o contraseña incorrectos")
            else:
                self.info_login = ctk.CTkLabel(self.root, text="Usuario o contraseña incorrectos")
                self.info_login.pack()
        else:
            if hasattr(self, "info_login"):
               self.info_login.configure(text=f"Hola, {obtener_usuario}. Espere unos instantes...")
            else:
                self.info_login = ctk.CTkLabel(self.root, text=f"Hola, {obtener_usuario}. Espere unos instantes...")
                self.info_login.pack()
                self.root.destroy()
            #Se instancia la ventana de opciones del programa
            Ventana_opciones = VentaOpciones()

class FuncionesPrograma:
    def ventana_consultas(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana de Consultas SQL")
        ventana.grab_set()
    
    #crear el frame para la ventana
        marco = ctk.CTkFrame(ventana)
        marco.pack(padx=10, pady=10)
    
    #crear el campo de texto para la consulta
        self.entrada = ctk.CTkEntry(marco, width=300)
        self.entrada.configure(font=fuentes_widgets)
        self.entrada.grid(row=0, column=0, pady=10)
    
    #Metodo para utilizar la logica del método consulta de base_datos.py
        def procesar_datos():
            try:
                #limpia el contenido del widget de texto
                self.texto.delete('1.0', 'end')
                #obtiene el contenido de la entrada
                datos = self.entrada.get()
                #llama al metodo base_datos.consulta() con los datos como argumento
                resultado = base_datos.consulta(datos)
                for registro in resultado:
                    self.texto.insert('end', registro)
                    self.texto.insert('end', '\n')
                #actualiza el contador de registros devueltos
                numero_registros = len(resultado)
                self.contador_registros.configure(text=f"Registros devueltos: {numero_registros}")
            except Exception:
                self.contador_registros.configure(text="Hay un error en la consulta SQL. Por favor, verifique.")
                CTkMessagebox(title="Error", message="Hay un error en la consulta SQL. Por favor, verifique.", icon="cancel")
                
    
    #crear el boton para enviar la consulta
        boton_envio = ctk.CTkButton(marco, text="Enviar", command=lambda : procesar_datos())
    
    #Posicionar el boton a la derecha del Entry()
        boton_envio.grid(row=0, column=1)
    
    #Crear el boton de borrado
        boton_borrar = ctk.CTkButton(marco, text="Borrar", command=self.limpiar_texto)
    #Posiciona el botón a la derecha del botón de envío
        boton_borrar.grid(row=0, column=2)
        
    #crear el widget de texto
        self.texto = ctk.CTkTextbox(marco, width=610, height=300)
        
    #Colocar el widget de texto debajo del Entry y el boton usando grid
        self.texto.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
    
    #Agrega un nuevo widget Label para mostrar el número de registros devueltos
        self.contador_registros = ctk.CTkLabel(marco, text="Esperando una instrucción...")
        self.contador_registros.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
    
    def limpiar_texto(self):
        #borra el contenido del widget de texto
        self.texto.delete('1.0', 'end')
    
    def ventana_crear_base_de_datos(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para crear base de datos")
        
    def ventana_eliminar_base_de_datos(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para eliminar base de datos")
        
    def ventana_crear_tabla(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para crear tabla")
    
    def ventana_eliminar_tabla(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para eliminar tabla")
        
    def ventana_insertar_registro(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para insertar registro")
    
    def ventana_copiar_base_de_datos(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para copiar base de datos")
    
    def ventana_mostrar_tablas(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para mostrar tablas")
   
    def ventana_eliminar_registro(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para eliminar registro")
    
    def ventana_actualizar_registro(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para actualizar registro")
   
    def ventana_mostrar_base_de_datos(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para mostrar base de datos")
        ventana.geometry("400x565")
        ventana.resizable(False, False)
        ventana.grab_set()
        
        #se crea el frame para la ventana
        marco = ctk.CTkFrame(ventana)
        marco.pack(padx=10, pady=10)
        
        #Se crea una etiqueta informativa para la ventana
        ctk.CTkLabel(marco, text="Listado de las bases de datos en el servidor: ", font=fuentes_widgets).pack(padx=10, pady=10)
        
        #Agregar un campo de entrada para la busqueda
        self.busqueda_control = tk.StringVar()   
        
        #se crea la entrda de texto para buquedas
        ctk.CTkEntry(marco, textvariable=self.busqueda_control, font=fuentes_widgets, width=300).pack(padx=10)
        
        self.texto = ctk.CTkTextbox(marco, width=300, height=300)
        self.texto.pack(padx=10, pady=10)
        
        #Se crea una etiqueta informativa para el número de bases de datos
        self.resultados_label = ctk.CTkLabel(marco, text="", font=fuentes_widgets)
        self.resultados_label.pack(padx=10, pady=10)
        
               
        #funcion interna de actualización SHOW DATABASES
        def actualizar():
            #Se establece el valor de la variable de control a string vacio
            self.busqueda_control.set("")
            #Se elimina el contenido de la caja de resultados
            self.texto.delete('1.0', 'end')
            #Se realiza la llamada al metodo mostrar_bd (SHOW DATABASES) y se guarda en resultado
            resultado = base_datos.mostrar_bd()
            #Se itera el resultado y se presenta linea a linea en la caja de texto.
            for bd in resultado:
                self.texto.insert('end', f"-> {bd[0]}\n")
            #Actualizar la etiqueta con el contenido de reaultados
            numero_resultados = len(resultado)
            if numero_resultados == 1:
                self.resultados_label.configure(text=f"Se encontró {numero_resultados} resultado.")
            else:
                self.resultados_label.configure(text=f"Se encontraron {numero_resultados} resultados.")
        
        #funcion interna de busqueda 
        def buscar():
            #Se elimina el contenido de la caja de resultados
            self.texto.delete('1.0', 'end')
            #Se re aliza la llamada al metodo mostrar_bd (SHOW DATABASES) y se guarda en resultado
            resultado = base_datos.mostrar_bd()
            #Se obtiene el valor dstring de la variable de control
            buscar = self.busqueda_control.get().lower()
            
            #Se crea una lista vacia donde almacenar los resultados filtrados
            resultado_filtrado = []
            #Se itera la tupla fetchall
            for bd in resultado:
                #Si lo que tiene la StringVar() esta en cada lista de la 
                if buscar in bd[0]:
                    #Se agrega a la lista vacia
                    resultado_filtrado.append(bd)   
            #Se itera la lista de resultados filtrados
            for bd in resultado_filtrado:
                #Se presenta linea a linea en la caja de texto
                self.texto.insert('end', f"-> {bd[0]}\n")
                
            #Se actualiza la etiqueta con el contenido de resultados
            numero_resultados = len(resultado_filtrado)
            if numero_resultados == 1:
                self.resultados_label.configure(text=f"Se encontró {numero_resultados} resultado.")
            else:
                self.resultados_label.configure(text=f"Se encontraron {numero_resultados} resultados.")

        #Se crea el botón para buscar las bases de datos
        boton_buscar = ctk.CTkButton(marco, text="Buscar", command=buscar)
        boton_buscar.pack(pady=10)

        #Se crea el botón para actualizar los resultados de la caja
        boton_actualizar = ctk.CTkButton(marco, text="Actualizar", command=actualizar)
        boton_actualizar.pack(pady=10)
        
        actualizar()
        
    def ventana_mostrar_columnas(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para mostrar columnas")
        
    def ventana_mostrar_registros(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para mostrar registros")
        
    def ventana_vaciar_tabla(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para vaciar tabla")
        
objetos_funciones = FuncionesPrograma()
    
class VentaOpciones:
    #Diccionario para los botones
    botones = {'Consulta SQL': objetos_funciones.ventana_consultas,
               'Crear base de datos': objetos_funciones.ventana_crear_base_de_datos,
                'Eliminar base de datos': objetos_funciones.ventana_eliminar_base_de_datos,
                'Crear tabla': objetos_funciones.ventana_crear_tabla,
                'Eliminar tabla': objetos_funciones.ventana_eliminar_tabla,
                'Insertar registro': objetos_funciones.ventana_insertar_registro,
                'Copiar base de datos': objetos_funciones.ventana_copiar_base_de_datos,
                'Mostrar tablas': objetos_funciones.ventana_mostrar_tablas,
                'Eliminar registro': objetos_funciones.ventana_eliminar_registro,
                'Actualizar registro': objetos_funciones.ventana_actualizar_registro,
                'Mostrar base de datos': objetos_funciones.ventana_mostrar_base_de_datos,
                'Mostrar columnas': objetos_funciones.ventana_mostrar_columnas,
                'Mostrar registros': objetos_funciones.ventana_mostrar_registros,
                'Vaciar tabla': objetos_funciones.ventana_vaciar_tabla        
    }
    
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Opciones para trabajar con bases de datos.")
        
        #Contador para la posición de los botones
        contador = 0
        
        #valor de elementos por fila
        elementos_fila = 3
        
        #crea los botones y establece su texto
        for texto_boton in self.botones:
            button = ctk.CTkButton(master=self.root, text=texto_boton, height=25, width=200, command=self.botones[texto_boton])
            button.grid(row=contador//elementos_fila, column=contador%elementos_fila, padx=5, pady=5)
            
            #incrementa el contador
            contador += 1
        self.root.mainloop()  