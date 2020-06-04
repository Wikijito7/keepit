import pymysql


# kipi
class BaseDatos:
    def __init__(self, host, user, passw, nombre_bd):
        self.conexion = pymysql.connect(host, user, passw, nombre_bd)
        self.cursor = self.conexion.cursor()

    def get_conexion(self):
        return self.conexion

    def select(self, tabla):  # bd.select("Categorias") -> lista con todas las categorias (select * from tabla)
        list_select = []
        self.cursor.execute("select * from " + tabla)
        rows = self.cursor.fetchall()  # Selecciona todo lo que contiene el cursor
        for row in rows:
            list_select.append(row)

        return list_select

    def usuario_login(self, email, password):
        """Login comprueba la entrada, consulta si existe en la bd y carga la instancia de Usuario"""
        if isinstance(email, str) and isinstance(password, str):
            self.cursor.execute("select * from usuario")
            #  lista_usuarios = [Usuario(user, passw) for user,passw in self.cursor.fetchall() if email == user and password == passw]
            for (user, passw) in self.cursor.fetchall():
                if email == user and password == passw:
                    return Usuario(email, password)
            return None
        else:
            # TODO mostrar warning
            pass

    def select_filtrado(self, tabla, parametros):  # lista con lo filtrado (select * from tabla where parametro)
        """Recibe una tupla, el primer parámetro de la tupla indica dónde busca y el segundo qué busca"""
        if isinstance(parametros, tuple) and len(parametros) == 2:
            # select * from tabla where algo = parametro // select * from usuario where email like %as%
            list_select = []
            regex = "'%" + str(parametros[1]) + "%'"
            # select * from usuario where email like '%st@%';
            self.cursor.execute("select * from " + tabla + " where " + parametros[0] + " like " + regex)

            rows = self.cursor.fetchall()
            for row in rows:
                list_select.append(row)
            return list_select
        else:
            # TODO: Añadir warning
            raise ValueError("Parámetros debe ser una tupla con dos parámetros.")

    def update(self, tabla, parametros: tuple):
        # TODO Pendiente de datle una vueltes
        if isinstance(parametros, tuple) and len(parametros) == 2:
            self.cursor.execute("update " + tabla + " set " + parametros[0] + " = " + parametros[1])
            self.conexion.commit()
        else:
            # TODO añadir warning
            raise ValueError("Debes introducir una tupla en el método update.")

    def update_nota(self, nota):
        self.cursor.execute("update notas set titulo = %s, contenido = %s, categoria = %s where id_notas = %s",
                            (nota.get_titulo(), nota.get_contenido(), nota.get_categoria(), str(nota.identificador)))

    def delete_etiquetas(self, id):
        # delete from notas_has_etiquetas where  = 305;
        self.cursor.execute("delete from notas_has_etiquetas where notas_id_notas = %s", id)
        self.conexion.commit()

    def delete_nota(self, id):
        self.cursor.execute("delete from notas where id_notas = %s", id)
        self.conexion.commit()

    def obtain_etiqueta(self, id):
        self.cursor.execute("select nombre from etiquetas where id_etiquetas = %s", id)
        return self.cursor.fetchall()

    def insert(self, tabla, datos: tuple):
        if isinstance(datos, tuple):
            # TODO HACK: Hacerlo de otra manera más entendible.
            args = ", ".join(("%s " * len(datos)).split())
            self.cursor.execute("insert into " + tabla + " values(" + args + ")", datos)
            self.conexion.commit()
        else:
            raise ValueError("Debes introducir una tupla en el método insert.")  # Paula quejica tq bb

    def obtain_last_id_notas(self):
        """
        execute a select to search id
        :return {int}: return last id_nota
        """
        self.cursor.execute("select max(id_notas) from Notas")
        return self.cursor.fetchall()[0][0]

    def obtain_id_etiquetas(self, etiqueta):
        """
        execute a select to search id
        :return {int}: return last id_etiquetas
        """
        self.cursor.execute("select id_etiquetas from Etiquetas where nombre like %s", etiqueta)
        try:
            return self.cursor.fetchall()[0][0]
        except IndexError:
            return None

    def exists_categoria(self, categoria):
        self.cursor.execute("select nombre from categorias where nombre like %s", categoria)
        if self.cursor.rowcount > 0:
            return True
        return False

    def exist_nota(self, titulo):
        self.cursor.execute("select * from notas where titulo like %s", titulo)
        if self.cursor.rowcount > 0:
            return True
        return False

    def delete_all_database(self):
        """Borra toda la base de datos"""
        self.cursor.execute("delete from usuario")
        self.cursor.execute("delete from notas")
        self.cursor.execute("delete from categorias")
        self.cursor.execute("delete from etiquetas")
        self.conexion.commit()

    def initial_insert(self):
        self.insert("usuario", ("test@test.es", "paulaquejica"))
        self.insert("usuario", ("guille@test.es", "Amapola"))
        self.insert("categorias", ("Alberti",))
        self.insert("notas", (None, "Exámen", "Preparar examen de prog", "Alberti", "test@test.es"))
        self.insert("etiquetas", ("Examenes", 1))
        id = self.obtain_last_id_notas()
        self.insert("Notas_has_Etiquetas", (id, 1))
        self.conexion.commit()


class Nota:
    def __init__(self, titulo, contenido, categoria, usuario, identificador, etiquetas=None):
        if isinstance(titulo, str) and isinstance(categoria, str) and isinstance(contenido, str) and isinstance(usuario,
                                                                                                                Usuario):
            self.titulo = titulo
            self.categoria = categoria  # ""
            self.contenido = contenido
            self.usuario = usuario
            self.identificador = identificador
            if etiquetas is None:
                self.etiquetas = []  # []
            elif isinstance(etiquetas, list):
                self.etiquetas = etiquetas
            else:
                raise ValueError("Las etiquetas deben venir dadas con una lista.")
        else:
            raise ValueError

    # getter and setters for Nota
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

    def get_titulo(self):
        return self.titulo

    def set_titulo(self, titulo):
        self.titulo = titulo

    def get_etiquetas_str(self):
        return ", ".join(self.etiquetas)

    def get_contenido(self):
        return self.contenido

    def set_contenido(self, contenido):
        self.contenido = contenido

    def get_as_list(self):
        return [self.identificador, self.titulo, self.categoria, self.usuario.get_email()]

    def __str__(self):
        return f"Nota(titulo: '{self.titulo}', categoría: '{self.categoria}', contenido: '{self.contenido}', usuario: '{self.usuario}', identificador: '{self.identificador}', etiquetas: '{self.etiquetas}')"


class Usuario:
    def __init__(self, email, password):
        if isinstance(email, str) and isinstance(password, str):
            self.email = email
            self.password = password

    def __str__(self):
        return f"Usuario('email':{self.email}', 'password':'{self.password}')"

    def get_email(self):
        return self.email


if __name__ == "__main__":
    # Test conexion clase BaseDatos
    bd = BaseDatos("localhost", "pepito", "grillo", "keepit")  # host, user, passw, nombre_bd

    # Test atributo execute clase BaseDatos
    bd.cursor.execute("select * from Categorias")
    print(bd.cursor.rowcount)
    bd.get_conexion().commit()
    bd.cursor.execute("delete from usuario")
    bd.conexion.commit()

    # Tests metodo insert clase BaseDatos
    bd.insert("usuario", ("test@test.es", "paulaquejica"))
    bd.insert("usuario", ("guille@test.es", "frantusmuerto"))

    #  print(bd.select("usuario"))
    print(bd.select_filtrado("usuario", ("email", "test@")))

    print(bd.usuario_login("guille@test.es", "frantusmuerto"))
