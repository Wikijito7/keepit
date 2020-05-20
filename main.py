import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter.ttk import Treeview
from keepit import *
import sys
import os


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
        for n in range(6):
            if n > len(self.notas)-1:
                break

            nota = self.notas[n]
            m = 3
            font_size = 12
            col = n % m
            row = 2 * m * (n // m)

            x, y = (308 + 185 * col, 238 + 30 * row)
            canvas = tk.Canvas(self.gui_notas)
            self.txt_titulo = tk.Label(self.gui_notas, text=nota.get_titulo(), wraplength=130,
                                       font=("Arial", font_size, "bold"), justify="center").place(x=x, y=y)
            self.btn_vereditar = tk.Button(self.gui_notas, text="Ver/Editar", width=12,
                                           font=("Arial", font_size)).place(x=x, y=y + 50)
            self.btn_eliminar = tk.Button(self.gui_notas, text="Eliminar", width=12, font=("Arial", font_size)).place(
                x=x, y=y + 90)

            canvas.create_rectangle(20, 20, 180, 170, outline="#000", width=2)
            canvas.place(x=x - 40, y=y - 30)

    def gui_notas_load_widgets(self):
        self.titulo = tk.Label(self.gui_notas, text="Keepit", font=("Arial", 20)).place(x=20, y=20)
        self.btn_buscar = tk.Button(self.gui_notas, text="Buscar", font=("Arial, 14"), width=12).place(x=846, y=20)
        self.btn_cerrar_sesion = tk.Button(self.gui_notas, text="Cerrar sesión", font=("Arial, 14"), width=12).place(x=846,
                                                                                                              y=700)
        self.load_gui_crear_notas = tk.Button(self.gui_notas, text="Nueva Nota", font=("Arial, 14"), width=12,
                                              command=self.load_gui_crear_notas).place(x=846,y=60)

        self.cargar_notas()
    def load_gui_crear_notas(self):
        CrearNotaGui(self.bd, self.notas, self.usuario, self.gui_notas)


class CrearNotaGui:
    def __init__(self, bd, notas, usuario, gui_notas):
        self.bd = bd
        self.notas = notas
        self.usuario = usuario
        self.gui_crea_notas = tk.Toplevel(gui_notas)
        self.gui_crea_notas.title("Kipi.gay v0.1")
        self.load_widgets_crea_nota()

    def anade_nota(self):
        titulo = self.input_titulo_nota.get()
        categoria = self.input_categoria_nota.get()
        etiqueta = self.input_etiqueta_nota.get()
        contenido = self.txt_contenido.get("1.0", 'end+1c')
        print(titulo)
        print(categoria)
        print(etiqueta)
        print(contenido)
        if titulo != "" and categoria != "" and etiqueta != "" and contenido != "":
            try:
                pass
                self.bd.insert("Categorias", ) #TODO: Terminar los insert en C N R
                """
                 def insert(self, tabla, datos: tuple):
                if isinstance(datos, tuple):
                    # TODO HACK: Hacerlo de otra manera más entendible.
                    args = ", ".join(("%s " * len(datos)).split())
                    self.cursor.execute("insert into " + tabla + " values(" + args + ")", datos)
                    self.conexion.commit()
                else:
                    raise ValueError("Debes introducir una tupla en el método insert.")  # Paula quejica tq bb
                """
            except:
                self.messagebox.showwarning("Alerta", "Datos ya existen en la agenda")

        else:
            messagebox.showwarning("Alerta", "Campos vacíos")

    def cancelar(self):
        self.gui_crea_notas.withdraw()  # close login

    def load_widgets_crea_nota(self):
        # TODO Colocar beautiful una vez que funcione [self.input_email.grid(column=0, row=1, columnspan=3, padx=20)]
        font_title = 20
        font_n = 12
        self.titulo_gui_notas = tk.Label(self.gui_crea_notas, text="Keepit", font=("Arial", font_title), width=30)
        self.titulo_gui_notas.pack()

        self.txt_titulo_nota = tk.Label(self.gui_crea_notas, text="Titulo", font=("Arial", font_n))
        self.txt_titulo_nota.pack()
        self.input_titulo_nota = tk.Entry(self.gui_crea_notas, width="40")
        self.input_titulo_nota.pack()

        self.txt_categoria_nota = tk.Label(self.gui_crea_notas, text="Categoria", font=("Arial", font_n))
        self.txt_categoria_nota.pack()
        self.input_categoria_nota = tk.Entry(self.gui_crea_notas, width="40")
        self.input_categoria_nota.pack()

        self.txt_etiqueta_nota = tk.Label(self.gui_crea_notas, text="Etiqueta", font=("Arial", font_n))
        self.txt_etiqueta_nota.pack()
        self.input_etiqueta_nota = tk.Entry(self.gui_crea_notas, width="40")
        self.input_etiqueta_nota.pack()

        self.txt_contenido_nota = tk.Label(self.gui_crea_notas, text="Contenido", font=("Arial", font_n))
        self.txt_contenido_nota.pack()
        self.txt_contenido = tk.Text(self.gui_crea_notas, height=10, width=40)
        self.txt_contenido.pack()

        self.btn_anade_nota = tk.Button(self.gui_crea_notas, text="añadir", width=10, height=2,
                                        command=self.anade_nota)
        self.btn_anade_nota.pack()

        self.btn_cancelar = tk.Button(self.gui_crea_notas, text="cancelar", width="10", height="2",
                                      command=self.cancelar)
        self.btn_cancelar.pack()


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
    # Usuario y contraseña
    manf = open("bd.txt", "r")
    # Test conexion clase BaseDatos
    bd = BaseDatos("localhost", manf.readline().rstrip(), manf.readline().rstrip(),
                   "keepit")  # host, user, passw, nombre_bd
    # Test atributo execute clase BaseDatos
    manf.close()
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
     self.btn_exit = tk.Button(self.gui_login, text="Exit", width="10", height="2",
                                  command=self.exit_login)
    """

    #  print(bd.select("usuario"))
    print(bd.select_filtrado("usuario", ("email", "test@")))

    print(bd.usuario_login("guille@test.es", "frantusmuerto"))

    # LoginRegisterGui(bd)
    usuario = bd.usuario_login("guille@test.es", "frantusmuerto")
    NotasGui(usuario, bd)
