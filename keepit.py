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

    def insert(self, tabla, datos: tuple):
        if isinstance(datos, tuple):
            # TODO HACK: Hacerlo de otra manera más entendible.
            args = ", ".join(("%s " * len(datos)).split())
            self.cursor.execute("insert into " + tabla + " values(" + args + ")", datos)
            self.conexion.commit()
        else:
            raise ValueError("Debes introducir una tupla en el método insert.")  # Paula quejica tq bb

    def obtain_id_notas(self):
        """
        execute a select to search id
        :return {int}: return last id_nota
        """
        self.cursor.execute("select max(id_notas) from Notas")
        return self.cursor.fetchall()[0][0]

    def obtain_id_etiquetas(self):
        """
        execute a select to search id
        :return {int}: return last id_etiquetas
        """
        self.cursor.execute("select max(id_etiquetas) from Etiquetas")
        return self.cursor.fetchall()[0][0]

    def check_exist(self, param):
        """
        check if param[1] in param[0]
        :param param {tuple}: param[0] = table param[1] == param
        :return {bool}: True if param[1] in param[0], False if not param[1] not in param[0]
        """
        if isinstance(param, tuple):
            self.cursor.execute("select * from " + param[0])
            for tupla in self.cursor.fetchall():
                if param[1] in tupla:
                    return True
            return False




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
    # asert bd.check_exists
    if bd.check_exist(("usuario","paulaquejica")):
        print("true")
    else:
        print("false")
