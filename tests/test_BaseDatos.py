"""
Tests de la clase Base de datos
Esta hace de conexión entre la aplicación y los datos
"""
import pytest

from keepit import *

# Instancia el objeto sobre el que se van a realizar las pruebas
# pepito y grillo es el usuario y la contraseña de la base de datos

bd_test = BaseDatos("localhost", "pepito", "grillo", "keepit")


def test_init():
    """
    Comprueba el constructor, este recibe 4 parámetro, y crea correctamente la instancia
    """
    # El constructor consta de 4 atributos
    servidor = "localhost"
    user = "pepito"
    passwd = "grillo"
    bd = "keepit"

    # Instancia el objeto correctamente
    assert BaseDatos(servidor, user, passwd, bd)
    bd_test_init = BaseDatos(servidor, user, passwd, bd)

    # Comprueba los atributos y su tipo
    # Atributo conexion
    assert type(bd_test_init.conexion) == pymysql.connections.Connection
    assert bd_test_init.conexion == bd_test_init.conexion
    # Atributo cursor
    assert type(bd_test_init.cursor) == pymysql.cursors.Cursor
    assert bd_test_init.cursor == bd_test_init.cursor


def test_get_conexion():
    """
    Comprueba el ge6er de conexión, si devuelve el tipo y la conexión
    """
    assert bd_test.get_conexion() == bd_test.conexion
    assert type(bd_test.get_conexion()) == pymysql.connections.Connection


def test_insert_delete_all():
    """
    Test de los inserts, la correcta insercción de los datos se comprobará mediante el método rowcount()
    Se realiza la misma para poder continuar cmoprobando el resto de métodos que dependen de que haya datos
    """

    bd_test.delete_all_database()

    # Comprueba método delete_all_dfatabase()
    bd_test.delete_all_database()
    bd_test.cursor.execute("Select * from usuario")
    assert bd_test.cursor.rowcount == 0
    bd_test.cursor.execute("Select * from categorias")
    assert bd_test.cursor.rowcount == 0
    bd_test.cursor.execute("Select * from notas")
    assert bd_test.cursor.rowcount == 0
    bd_test.cursor.execute("Select * from etiquetas")
    assert bd_test.cursor.rowcount == 0
    bd_test.cursor.execute("select * from Notas_has_Etiquetas")
    assert bd_test.cursor.rowcount == 0

    # Insección en tabla usuario
    bd_test.insert("usuario", ("test@test.es", "paulaquejica"))
    bd_test.insert("usuario", ("guille@test.es", "Amapola"))
    bd_test.cursor.execute("Select * from usuario")
    assert bd_test.cursor.rowcount == 2

    # Insercción tabla categoria
    bd_test.insert("categorias", ("Alberti",))
    bd_test.insert("categorias", ("Personal",))
    bd_test.cursor.execute("Select * from categorias")
    assert bd_test.cursor.rowcount == 2

    # Insercción tabla notas (id autonumerado, titulo, contenido, categoria, usuario)
    bd_test.insert("notas", (None, "Examen", "Preparar examen de prog", "Alberti", "test@test.es"))
    bd_test.insert("notas", (None, "Comunion", "Buscar chaqueta para la comunion", "Personal", "guille@test.es"))
    bd_test.cursor.execute("Select * from notas")
    assert bd_test.cursor.rowcount == 2

    # Insercción tabla etiquetas
    bd_test.insert("etiquetas", ("Examenes", 1))
    bd_test.insert("etiquetas", ("Reuniones", 2))
    bd_test.cursor.execute("Select * from etiquetas")
    assert bd_test.cursor.rowcount == 2

    # Insercción tabla Notas_has_Etiquetas. Para ello es necesario obtener el id de la última nota obtain_id_notas
    id_nota = bd_test.obtain_last_id_notas()
    bd_test.insert("Notas_has_Etiquetas", (id_nota, 1))

    id_nota = bd_test.obtain_last_id_notas()
    bd_test.insert("Notas_has_Etiquetas", (id_nota, 2))

    bd_test.cursor.execute("select * from Notas_has_Etiquetas")
    assert bd_test.cursor.rowcount == 2

    # Comprueba método delete_all_dfatabase()
    bd_test.delete_all_database()
    bd_test.cursor.execute("Select * from usuario")
    assert bd_test.cursor.rowcount == 0
    bd_test.cursor.execute("Select * from categorias")
    assert bd_test.cursor.rowcount == 0
    bd_test.cursor.execute("Select * from notas")
    assert bd_test.cursor.rowcount == 0
    bd_test.cursor.execute("Select * from etiquetas")
    assert bd_test.cursor.rowcount == 0
    bd_test.cursor.execute("select * from Notas_has_Etiquetas")
    assert bd_test.cursor.rowcount == 0


def test_initial_insert_select():
    """
    Comprueba la insercción por defecto de los datos, la comprobación se realizará mediante el método select()
    el cuál devuelve una lista compuesta de una tupla por registro.
    El método select() devuelve una lista con todos los registros de una tabla
    """
    # Se insertan los datos por defecto
    bd_test.initial_insert()

    # Comprueba que se insertan los dos usuarios por defecto
    bd_test.cursor.execute("Select * from usuario")
    assert bd_test.cursor.rowcount == 2
    assert bd_test.select("usuario") == [('guille@test.es', 'Amapola'), ('test@test.es', 'paulaquejica')]

    # Comprueba que se inserta la categoría por defecto
    bd_test.cursor.execute("Select * from categorias")
    assert bd_test.cursor.rowcount == 1
    assert bd_test.select("categorias") == [('Alberti',)]

    # Comprueba que se inserta la nota por defecto
    bd_test.cursor.execute("Select * from notas")
    assert bd_test.cursor.rowcount == 1
    id_nota = bd_test.obtain_last_id_notas()  # El id de la nota se inserta por defectp por ello utilizamos este métdo
    assert bd_test.select("notas") == [(id_nota, 'Exámen', 'Preparar examen de prog', 'Alberti', 'test@test.es')]

    # Comprueba que se inserta la etiqueta por defecto
    bd_test.cursor.execute("Select * from etiquetas")
    assert bd_test.cursor.rowcount == 1
    assert bd_test.select("etiquetas") == [('Examenes', 1)]

    # Comprueba la tabla notas_has_etiquetas
    bd_test.cursor.execute("Select * from Notas_has_Etiquetas")
    assert bd_test.cursor.rowcount == 1
    assert bd_test.select("Notas_has_Etiquetas") == [(id_nota, 1)]


def test_usuario_login():
    """
    Comprueba siel usuario existe para hacer el login
    Si este se encuentra en la tabla de usuarios se logea si devuelve None
    :return Usuario Object: Si el usuario existe, None si el usuario no existe
    """
    # El usuario existe devuelve un objeto de tipo Usuario con sus datos
    assert bd_test.usuario_login("guille@test.es", "Amapola")
    usu = bd_test.usuario_login("guille@test.es", "Amapola")
    assert usu.email == "guille@test.es"
    assert usu.password == "Amapola"
    # El usuario no existe decuelve None
    assert bd_test.usuario_login("no_existo@test.es", "no_existo") is None


def test_select_filter():
    """
    Comprueba que la función select filter decuelve una lista del resultado de hacer una consulta
    a partir de una tabla, y dos parámetros columna y valor
    :return list: contenido del select
    """

    # devuelve de la tabla de usuasrios los usuarios que contengan en su correo @test.es
    assert bd_test.select_filtrado("usuario", ("email", "@test")) == [('guille@test.es', 'Amapola'),
                                                                      ('test@test.es', 'paulaquejica')]
    # devuelve solo los usuarios que contenga pola en su contrasena
    assert bd_test.select_filtrado("usuario", ("contrasena", "pola")) == [('guille@test.es', 'Amapola')]

    # devuelve una lista vacia al no contener nada
    assert bd_test.select_filtrado("usuario", ("email", "zs")) == []


def test_exists_nota():
    """
    Comprueba si existe la nota a partir de su titulo
    :returns bool: True si existe la nota, False si no existe la nota
    """
    # La nota con título examen existe
    assert bd_test.exist_nota("Examen") == True
    # La nota con título prueba no existe
    assert bd_test.exist_nota("Prueba") == False


def test_exists_categoria():
    """
    Comprueba si existe la categoría
    :returns bool: True si existe, False si no existe
    """
    # La categoría Alberti existe
    assert bd_test.exists_categoria("Alberti") == True

    # La categoría Drago no existe
    assert bd_test.exists_categoria("Drago") == False


def test_update_nota():
    """
    Recibe como argumento una nota que actualiza la que ya existia a parit de un identificador
    """
    # Introduzco una nota nueva y etiqueta
    bd_test.insert("categorias", ("Viajes",))
    bd_test.insert("notas", (None, "Madrid", "Preparar el coche para el vieaje", "Viajes", "test@test.es"))
    # bd_test.insert("etiquetas", ("Verano", 2))

    # Comprobamos la nota que acabo de añadir
    id = bd_test.obtain_last_id_notas()
    assert bd_test.select_filtrado("notas", ("id_notas", id)) == [(id, 'Madrid', 'Preparar el coche para el vieaje',
                                                                   'Viajes', 'test@test.es')]
    # Preparamos una instancia de Nota con la misma id para sustituirla por la que antes tenia su id
    # La instanciamos
    nota_updated = Nota("Barcelona", "Preaprar carabana para el viaje", "Viajes",
                        Usuario("test@test.es", "paulaquejica"), id, [])
    bd_test.update_nota(nota_updated)

    # Comprobamos si se ha actualizado
    assert bd_test.select_filtrado("notas", ("id_notas", id)) == [(id, 'Barcelona', 'Preaprar carabana para el viaje',
                                                                   'Viajes', 'test@test.es')]


def test_obtain_last_id_notas():
    """
    Comprueba si el método obtiene la última id de notas, Lo comprobaré mediante una consulta
    de la ultima id
    """
    # Obtengo la última id
    bd_test.cursor.execute("Select max(id_notas) from Notas")
    # Comprueba si coincide con la id devuelta por el método
    assert bd_test.cursor.fetchall()[0][0] == bd_test.obtain_last_id_notas()


def test_obtain_id_etiquetas():
    """
    Comprueba si el método devuelve el id de la etiqueta seleccionada
    """
    # Obtengo la última id
    n_etiqueta = "Examenes"
    # Realizp la consulta
    bd_test.cursor.execute("select id_etiquetas from Etiquetas where nombre like '" + n_etiqueta + "'")
    # Compruebo si devuleve lo mismo
    assert bd_test.cursor.fetchall()[0][0] == bd_test.obtain_id_etiquetas(n_etiqueta)


def test_obtain_etiqueta():
    """
    Comprueba si se devuelve una lista con la etiqueta a partir de la id, lo comprobaré mediante el método select(),
    """
    # Obtengo la id de las etiquetas
    id_etiqueta = bd_test.obtain_id_etiquetas("Examenes")
    # Saviendo que la id corresponde a Examenes la comparo directamente con Examenes
    assert bd_test.obtain_etiqueta(id_etiqueta)[0][0] == "Examenes"


# Elimino los datos de la base de datos al final el test de su clase
bd_test.delete_all_database()
