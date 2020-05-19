import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter.ttk import Treeview
from keepit import *
import sys


class LoginRegisterGui:
    # TODO Crear el formulario de login/register
    def __init__(self, bd):
        self.gui_login = tk.Tk()
        self.bd = bd
        self.conexion = bd.conexion

        # Cargar componentes y demases del programa.
        self.gui_login.title("Kipi.gay v0.1")  # Paula quejica
        self.load_widgets_login()
        self.gui_login.mainloop()

    def login(self):
        if self.input_email.get() != "" and self.input_passw.get() != "":
            usuario = self.bd.usuario_login(self.input_email.get(),
                                            self.input_passw.get())  # TODO: Coger del layout los textfield y pasar los parametros
            if usuario is None:
                messagebox.showwarning("Error", "Error de credenciales")
            else:
                self.gui_login.withdraw()  # cierra la ventana si no se hace asi no funciona 100% comprobado por mi
                NotasGui(usuario, self.bd)

    def register(self):
        if self.input_email.get() != "" and self.input_passw.get() != "":
            usuario = self.bd.usuario_login(self.input_email.get(),
                                            self.input_passw.get())  # TODO: Coger del layout los textfield y pasar los parametros
            if usuario is None:
                bd.insert("usuario", (self.input_email.get(), self.input_passw.get()))
                self.login()
            else:
                messagebox.showwarning("Error", "Ese usuario ya está registrado.")

    def exit_login(self):
        self.gui_login.destroy()  # Guille rojo :)
        sys.exit()

    def load_widgets_login(self):
        self.txt_email = tk.Label(self.gui_login, text="Introduce tu email")
        self.txt_email.grid(column=0, row=0, columnspan=3, pady=(20, 5), padx=20)

        self.input_email = tk.Entry(self.gui_login, width=40)
        self.input_email.grid(column=0, row=1, columnspan=3, padx=20)

        self.txt_passw = tk.Label(self.gui_login, text="Introduce tu contraseña")
        self.txt_passw.grid(column=0, row=2, columnspan=3, pady=(20, 5), padx=20)

        self.input_passw = tk.Entry(self.gui_login, show="*", width=40)
        self.input_passw.grid(column=0, row=3, columnspan=3, padx=20)

        self.btn_login = tk.Button(self.gui_login, text="Login", width="10", height="2",
                                   command=self.login)
        self.btn_login.grid(column=0, row=4, pady=20, padx=10)

        self.btn_register = tk.Button(self.gui_login, text="Register", width="10", height="2",
                                      command=self.register)
        self.btn_register.grid(column=1, row=4, pady=20, padx=10)

        self.btn_exit = tk.Button(self.gui_login, text="Exit", width="10", height="2",
                                  command=self.exit_login)
        self.btn_exit.grid(column=2, row=4, pady=20, padx=10)

        #  l1.grid(row=0, column=0, padx=(100, 10)) izq derc
        #  l2.grid(row=1, column=0, pady=(10, 100)) arriba abajo


# .tq bb yo tambien :) shh
class NotasGui:
    # TODO Crear el formulario de las notas
    def __init__(self, usuario, bd):
        self.gui_notas = tk.Tk()
        self.bd = bd
        self.usuario = usuario
        self.notas = []
        self.gui_notas.geometry("1024x768")
        self.gui_notas.title("Kipi.gay v0.1")
        self.obtener_notas()
        self.gui_notas_load_widgets()
        self.gui_notas.mainloop()

    def obtener_notas(self):
        notas_temporales = self.bd.select_filtrado("notas", ("Usuario_email", self.usuario.get_email()))
        # titulo, contenido, categoria, usuario, identificador, etiquetas = None
        for nota in notas_temporales:
            etiquetas = []
            etiquetas_id = self.bd.select_filtrado("Notas_has_Etiquetas", ("Notas_id_notas", nota[0]))
            for etiqueta_id in etiquetas_id:
                etiqueta = self.bd.select_filtrado("etiquetas", ("id_etiquetas", etiqueta_id[1]))
                etiquetas.append(etiqueta[0][0])
            self.notas.append(Nota(nota[1], nota[2], nota[3], self.usuario, nota[0], etiquetas))
        for nota in self.notas:
            print(nota)

    def cargar_notas(self):
        self.titulo = tk.Label(self.gui_notas, text="Keepit")
        self.titulo.config(font=("Arial", 20))
        self.titulo.grid(column=0, row=0)

        for n in range(6):
            if n > len(self.notas) - 1:
                break

            nota = self.notas[n]
            m = 3
            col = n % m
            row = 2 * m * (n // m)

            x, y = (328 + 160 * col, 278 + 20 * row)

            self.txt_titulo = tk.Label(self.gui_notas, text=f"{nota.get_titulo()}").place(x=x, y=y)
            self.txt_categoria = tk.Label(self.gui_notas, text=f"{nota.get_categoria()}").place(x=x, y=y + 20)
            if len(nota.etiquetas) > 0:
                self.txt_etiquetas = tk.Label(self.gui_notas, text=f"{nota.get_etiquetas_str()}").place(x=x, y=y + 40)
            else:
                self.txt_etiquetas = tk.Label(self.gui_notas, text="Sin etiquetas").place(x=x, y=y + 40)
            self.txt_contenido = tk.Label(self.gui_notas, text=f"{nota.get_contenido()}", justify="left", wraplength=120).place(x=x, y=y + 60)

    def gui_notas_load_widgets(self):
        self.cargar_notas()


class CrearNotaGui:
    # TODO Crear el formulario de añadir una nueva nota
    pass


class ModNotasGui:
    # TODO Crear el formulario de modificar la nota
    pass


class BusquedaGui:
    # TODO Crear el formulario de busqueda
    pass


# Crear el formulario de login/register
# Crear el formulario de las notas
# Crear el formulario de añadir una nueva nota
# Crear el formulario de modificar la nota
# Crear el formulario de busqueda


if __name__ == "__main__":
    # Test conexion clase BaseDatos
    bd = BaseDatos("localhost", "root", "root", "keepit")  # host, user, passw, nombre_bd
    # Test atributo execute clase BaseDatos
    bd.cursor.execute("delete from usuario")
    bd.cursor.execute("delete from notas")
    bd.cursor.execute("delete from categorias")
    bd.cursor.execute("delete from etiquetas")
    bd.conexion.commit()

    # Tests metodo insert clase BaseDatos 
    bd.insert("usuario", ("test@test.es", "paulaquejica"))
    bd.insert("usuario", ("guille@test.es", "frantusmuerto"))

    bd.insert("categorias", ("paula",))
    bd.insert("categorias", ("escocia",))

    bd.insert("notas", (None, "Quejica", "Eres una quejica", "paula", "guille@test.es"))
    bd.insert("notas", (None, "Lloro", "hola soy un llorica Davileño", "escocia", "guille@test.es"))

    bd.insert("etiquetas", ("quejas", 1))

    id = bd.obtain_id()
    bd.insert("Notas_has_Etiquetas", (id, 1))


    """
        insert into categorias
    values("paula"),
        ("escocia");
    
    insert into notas(titulo, contenido, categoria, usuario_email)
    values("Quejica","Eres una quejica","paula","guille@test.es"),
        ("Lloro","hola soy un llorica Antonio", "escocia","guille@test.es");
    """

    #  print(bd.select("usuario"))
    print(bd.select_filtrado("usuario", ("email", "test@")))

    print(bd.usuario_login("guille@test.es", "frantusmuerto"))

    #LoginRegisterGui(bd)
    usuario = bd.usuario_login("guille@test.es", "frantusmuerto")
    NotasGui(usuario, bd)
