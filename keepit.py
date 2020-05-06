# import pymysql
from tkinter import *

# connection = pymysql.connect(host='localhost',
#                              user='user',
#                              password='passwd',
#                              db='db',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)


class Nota:
    def __init__(self, titulo, contenido, categoria, usuario, identificador, etiquetas = None):
        if isinstance(titulo, str) and isinstance(categoria, str) and isinstance(contenido, str) and isinstance(usuario, Usuario):
            self.titulo = titulo
            self.categoria = categoria # ""
            self.contenido = contenido
            self.usuario = usuario
            self.identificador = identificador
            if etiquetas == None:
                self.etiquetas = [] # []
            elif isinstance(etiquetas, list):
                self.etiquetas = etiquetas
            else:
                raise ValueError("Las etiquetas deben venir dadas con una lista.")
        else:
            raise ValueError

    #getter and setters for Nota
    def get_etiquetas(self):
        return self.etiquetas

    def set_etiquetas(self, nuevas_etiquetas: list):
        if isinstance(nuevas_etiquetas, list):
            self.etiquetas = nuevas_etiquetas

    def add_etiqueta(self, etiqueta: str):
        if isinstance(etiqueta, str) and etiqueta not in self.etiquetas:
            self.etiquetas.append(etiqueta)


            
        
    def get_categoria(self):
        return self.categoria


    def set_categoria(self, nueva_categoria: str):
        if isinstance(nueva_categoria, str):
            self.categoria = nueva_categoria
        

class Usuario:
    def __init__(self, email, password):
        if isinstance(email, str) and ininstance(password, str):
            self.email = email
            self.password = password
    
    def __str__(self):
        return f"Usuario('email':{self.email}, 'password':{self.password})"
    
    def get_email(self):
        return self.email


"""
https://python-textbok.readthedocs.io/en/1.0/Introduction_to_GUI_Programming.html
"""
# TODO: Acabar los métodos
# HACK: Hacerlo todo más eficiente y bonito.
class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("Keepit") # una ventana

        self.label = Label(master, text="Etiqueta de prueba") # una etiqueta
        self.label.pack() #TODO: hacerlo bonito

        self.btnFiltrar = Button(master, text="Filtrar", command=self.filtrar) # boton
        self.btnFiltrar.pack()

        self.btnAtras = Button(master, text="Atrás", command=self.volver_atras) # boton
        self.btnAtras.pack()

        self.btnLogin = Button(master, text="Iniciar sesión", command=self.login) # boton
        self.btnLogin.pack()

        self.btnLogout = Button(master, text="Cerrar sesión", command=self.logout) # boton
        self.btnLogout.pack()

        self.btnSalir = Button(master, text="Cerrar", command=exit()) # boton
        self.btnSalir.pack()

    def filtrar(self):
        # Recibe palabras claves por input
        # Ejecutar consulta a la bd
        # 
        """
        palabras_clave = self.textField.get_text()
        
        notas_seleccionadas = resultado ejecutar la consulta de sql -> 
        """
        pass

    def volver_atras(self):
        # Vuelve a la ventana anterior
        pass

    def login(self):
        # Recibe usuario y contraseña por input
        # Si está en la bd loguea
        # Si no está, crea nuevo usuario y loguea
        pass 
    
    def logout(self):
        # Cierra sesión
        # Vuelve a pantalla de inicio de sesión
        pass

    

if __name__ == "__main__":

    root = Tk()
    my_gui = MyFirstGUI(root)
    root.mainloop()

"""
Button(master, text="Close", command=master.quit)
    -> master: donde está el boton.
    -> text: el texto que apaerece dentro del boton.
    -> command: lo que se ejecuta al hacerle click

btnFiltrar = Button(master, text="paula quejica", command=filtrar(palabras_clave))
"""



"""
    loquesea = consultamysql -> 15*(notas)
    Nota(contenido que hemos obtenido de la consulta)

    a. Al cargar el programa, se generan las notas del usuario. Filtrado, borrado, etc se hace en codigo interno. Al cerrar o periodicamente
        se le informa a la base.
        TODO: añadir botón guardar en la nube.

    b. No hay notas, cargamos temporalmente todas las notas. Filtrado -> borramos notas, hacemos consulta para generar nuevos objetos
        Nota. Cada vez que hay modificaciones, se crean o eliminan notas, hay que informarle a la base.
"""