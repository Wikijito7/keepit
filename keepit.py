import pymysql
from tkinter import *

class Usuario:
    pass

class Nota:
    def __init__(self, titulo, contenido, categoria, usuario, etiquetas = None):
        if isinstance(titulo, str) and isinstance(categoria, str) and isinstance(contenido, str) and isinstance(usuario, Usuario):
            self.titulo = titulo
            self.categoria = categoria
            self.contenido = contenido
            self.usuario = usuario
            if etiquetas == None:
                self.etiquetas = []
            elif isinstance(etiquetas, list):
                self.etiquetas = etiquetas
            else:
                raise ValueError("Las etiquetas deben venir dadas con una lista.")
        else:
            raise ValueError

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