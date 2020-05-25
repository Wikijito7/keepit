import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter.ttk import Treeview
from keepit import *
import sys
import os


class LoginRegisterGui:
    def __init__(self, bd):
        self.gui_login = tk.Tk()
        self.bd = bd
        self.conexion = bd.conexion

        # Cargar componentes y demases del programa.
        self.gui_login.resizable(0, 0)
        self.gui_login.title("Keepit v0.1")  # Paula quejica
        self.load_widgets_login()
        self.gui_login.mainloop()

    def login(self):
        if self.input_email.get() != "" and self.input_passw.get() != "":
            usuario = self.bd.usuario_login(self.input_email.get(),
                                            self.input_passw.get())
            if usuario is None:
                messagebox.showwarning("Error", "Error de credenciales")
            else:
                self.gui_login.withdraw()  # cierra la ventana si no se hace asi no funciona 100% comprobado por mi
                NotasGui(usuario, self.bd)

    def register(self):
        if self.input_email.get() != "" and self.input_passw.get() != "":
            usuario = self.bd.usuario_login(self.input_email.get(),
                                            self.input_passw.get())
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
    def __init__(self, usuario, bd):
        self.gui_notas = tk.Tk()
        self.bd = bd
        self.usuario = usuario
        self.notas = []
        self.rango_notas = 0
        # Cargamos la interfaz.
        self.gui_notas.resizable(0, 0)
        self.gui_notas.geometry("1024x768")
        self.gui_notas.title("Keepit v0.1")
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

    def cargar_notas(self):
        for n in range(6):
            m = 3
            font_size = 10
            col = n % m
            row = 2 * m * (n // m)
            canvas = tk.Canvas(self.gui_notas)
            x, y = (202 + 220 * col, 228 + 32 * row)
            try:
                nota = self.notas[self.rango_notas + n - 1]

                if n == 0:
                    tk.Button(self.gui_notas, text="+", font=("Arial", 33, "bold"), width=6, height=2,
                              borderwidth=1, command=self.load_gui_crear_notas).place(x=x - 10, y=y + 5)
                else:
                    tk.Label(self.gui_notas, text=nota.get_titulo(), wraplength=150, font=("Arial", font_size, "bold"),
                             justify="center").place(x=x, y=y)

                    self.boton_vereditar = tk.Button(self.gui_notas, text="Ver/Editar", width=17, font=("Arial", font_size),
                                                     command=lambda i=nota: self.load_gui_crear_notas(i))
                    self.boton_vereditar.place(x=x, y=y + 80)
                    self.eliminar = tk.Button(self.gui_notas, text="Eliminar", width=17, font=("Arial", font_size),
                                              command=lambda i=nota: self.eliminar_nota(i.identificador))
                    self.eliminar.place(x=x, y=y + 110)
                canvas.create_rectangle(20, 20, 210, 190, outline="#000", width=2)
            except IndexError:
                canvas.create_rectangle(20, 20, 210, 190, width=0)
                self.next_page.place(x=1024)
            else:
                self.next_page.place(x=20)
            canvas.place(x=x - 40, y=y - 30)

    def gui_notas_load_widgets(self):
        self.titulo = tk.Label(self.gui_notas, text="Keepit", font=("Arial", 20)).place(x=20, y=20)
        self.btn_buscar = tk.Button(self.gui_notas, text="Buscar", font=("Arial", 14), width=12).place(x=846, y=20)
        self.btn_cerrar_sesion = tk.Button(self.gui_notas, text="Cerrar sesión", font=("Arial", 14),
                                           width=12, command=self.cerrar_sesion).place(x=846, y=700)
        self.next_page = tk.Button(self.gui_notas, text="Siguiente", font=("Arial, 14"), width=10,
                                   command=self.pagina_siguiente)
        self.next_page.place(x=20, y=222)

        self.previous_page = tk.Button(self.gui_notas, text="Anterior", font=("Arial, 14"), width=10,
                                       command=self.pagina_anterior)
        self.previous_page.place(x=1024, y=532)
        self.cargar_notas()

    def load_gui_crear_notas(self, nota=None):
        CrearNotaGui(self.bd, self.usuario, self.gui_notas, self, nota)

    def cerrar_sesion(self):
        self.gui_notas.withdraw()
        LoginRegisterGui(bd)

    def pagina_siguiente(self):
        if self.rango_notas + 6 <= len(self.notas):
            self.rango_notas += 5
            self.previous_page.place(x=20)
            self.cargar_notas()
            print(self.rango_notas, self.rango_notas + 6, len(self.notas))

    def pagina_anterior(self):
        if self.rango_notas - 5 >= 0:
            self.rango_notas -= 5
            self.cargar_notas()
            self.next_page.place(x=20)

        if self.rango_notas == 0:
            self.previous_page.place(x=1024)

    def recargar_notas(self):
        self.notas = []
        self.obtener_notas()
        self.cargar_notas()

    def eliminar_nota(self, id):
        self.bd.delete_nota(id)
        self.recargar_notas()


class CrearNotaGui:
    def __init__(self, bd, usuario, gui_notas, interf_principal, nota=None):
        self.bd = bd
        self.edit_mode = False
        if nota is None:
            self.nota = Nota("", "", "", usuario, 0)
        else:
            self.edit_mode = True
            self.nota = nota

        self.usuario = usuario

        # Cargamos la interfaz.
        self.gui_notas = interf_principal
        self.gui_crea_notas = tk.Toplevel(gui_notas)
        self.gui_crea_notas.resizable(0, 0)
        self.gui_crea_notas.title("Keepit v0.1")
        self.load_widgets_crea_nota()

    def anade_nota(self):
        # TODO: Rehacer todo el método para hacerlo funcionar acorde al programa real.
        titulo = self.input_titulo_nota.get()
        categoria = self.input_categoria_nota.get()
        etiqueta = self.input_etiqueta_nota.get()
        contenido = self.txt_contenido.get("1.0", 'end+1c')
        if titulo != "" and categoria != "":
            if not self.bd.exists_categoria(categoria):
                self.bd.insert("Categorias", (categoria,))

            etiquetas = []

            if etiqueta != "":
                etiquetas = etiqueta.split(",")

            if not self.bd.exist_nota(titulo) and not self.edit_mode:
                self.bd.insert("Notas", (None, titulo, contenido, categoria, self.usuario.email))
            elif self.edit_mode:
                self.bd.update_nota(Nota(titulo, contenido, categoria, self.nota.usuario, self.nota.identificador, etiquetas))
                self.bd.delete_etiquetas(self.nota.identificador)
            else:
                messagebox.showwarning("Alerta", "Esa etiqueta ya existe. Prueba a darle a Ver/Editar.)")

            for etiqueta in etiquetas:
                etiqueta = etiqueta.lstrip(" ")
                if self.bd.obtain_id_etiquetas(etiqueta) is None:
                    self.bd.insert("etiquetas", (etiqueta, None))
                if not self.edit_mode:
                    self.bd.insert("Notas_has_Etiquetas", ((self.bd.obtain_last_id_notas()), self.bd.obtain_id_etiquetas(etiqueta)))
                else:
                    self.bd.insert("Notas_has_Etiquetas", (self.nota.identificador, self.bd.obtain_id_etiquetas(etiqueta)))
            self.gui_notas.recargar_notas()
            self.gui_crea_notas.withdraw()
        else:
            messagebox.showwarning("Alerta", "Titulo y categoría, deben estar rellenos")

    def cancelar(self):
        self.gui_crea_notas.withdraw()

    def load_widgets_crea_nota(self):
        # TODO Colocar beautiful una vez que funcione [self.input_email.grid(column=0, row=1, columnspan=3, padx=20)]
        font_title = 20
        font_n = 12
        self.titulo_gui_notas = tk.Label(self.gui_crea_notas, text="Keepit", font=("Arial", font_title), width=30)
        self.titulo_gui_notas.grid(column=0, row=0, columnspan=3, pady=20)

        self.txt_titulo_nota = tk.Label(self.gui_crea_notas, text="Titulo", font=("Arial", font_n))
        self.txt_titulo_nota.grid(column=0, row=1, columnspan=3, pady=(10, 5), padx=20)

        self.input_titulo_nota = tk.Entry(self.gui_crea_notas, width="40")
        self.input_titulo_nota.insert(tk.END, self.nota.get_titulo())
        self.input_titulo_nota.grid(column=0, row=2, columnspan=3, padx=20)

        self.txt_categoria_nota = tk.Label(self.gui_crea_notas, text="Categoria", font=("Arial", font_n))
        self.txt_categoria_nota.grid(column=0, row=3, columnspan=3, pady=(10, 5), padx=20)

        self.input_categoria_nota = tk.Entry(self.gui_crea_notas, width="40")
        self.input_categoria_nota.insert(tk.END, self.nota.get_categoria())
        self.input_categoria_nota.grid(column=0, row=4, columnspan=3, padx=20)

        self.txt_etiqueta_nota = tk.Label(self.gui_crea_notas, text="Etiqueta", font=("Arial", font_n))
        self.txt_etiqueta_nota.grid(column=0, row=5, columnspan=3, pady=(10, 5), padx=20)

        self.input_etiqueta_nota = tk.Entry(self.gui_crea_notas, width="40")
        self.input_etiqueta_nota.insert(tk.END, self.nota.get_etiquetas_str())
        self.input_etiqueta_nota.grid(column=0, row=6, columnspan=3, padx=20)

        self.txt_contenido_nota = tk.Label(self.gui_crea_notas, text="Contenido", font=("Arial", font_n))
        self.txt_contenido_nota.grid(column=0, row=7, columnspan=3, pady=(10, 5), padx=20)

        self.txt_contenido = tk.Text(self.gui_crea_notas, height=10, width=52)
        self.txt_contenido.insert(tk.END, self.nota.get_contenido())
        self.txt_contenido.grid(column=0, row=8, columnspan=3, padx=20)

        self.btn_anade_nota = tk.Button(self.gui_crea_notas, text="Añadir", width=14, height=2, font=("Arial", 11),
                                        command=self.anade_nota)
        self.btn_anade_nota.grid(column=0, row=9, pady=20)

        self.btn_cancelar = tk.Button(self.gui_crea_notas, text="Cancelar", width=14, height=2, font=("Arial", 11),
                                      command=self.cancelar)
        self.btn_cancelar.grid(column=2, row=9, pady=20)


class BusquedaGui:
    # TODO Crear el formulario de busqueda
    pass


# Crear el formulario de login/register DONE
# Crear el formulario de las notas DONE
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
    # bd.cursor.execute("delete from usuario")
    # bd.cursor.execute("delete from notas")
    # bd.cursor.execute("delete from categorias")
    # bd.cursor.execute("delete from etiquetas")
    bd.conexion.commit()

    # Tests metodo insert clase BaseDatos 
    # bd.insert("usuario", ("test@test.es", "paulaquejica"))
    # bd.insert("usuario", ("guille@test.es", "frantusmuerto"))
    #
    # bd.insert("categorias", ("paula",))
    # bd.insert("categorias", ("escocia",))
    #
    # bd.insert("notas", (None, "Quejica", "Eres una quejica", "paula", "guille@test.es"))
    # bd.insert("notas", (None, "Lloro", "hola soy un llorica Davileño", "paula", "guille@test.es"))
    #
    # bd.insert("etiquetas", ("quejas", 1))
    #
    # id = bd.obtain_id_notas()
    # bd.insert("Notas_has_Etiquetas", (id, 1))

    """
     self.btn_exit = tk.Button(self.gui_login, text="Exit", width="10", height="2",
                                  command=self.exit_login)
    """

    #  print(bd.select("usuario"))
    print(bd.select_filtrado("usuario", ("email", "test@")))
    print(bd.select("Categorias"))

    print(bd.usuario_login("guille@test.es", "frantusmuerto"))

    # LoginRegisterGui(bd)
    usuario = bd.usuario_login("guille@test.es", "frantusmuerto")
    NotasGui(usuario, bd)
