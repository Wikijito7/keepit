"""
Tests de la clase Base de datos
Esta hace de conexión entre la aplicación y los datos
"""
import pytest

from ProyectoEEDES.keepit import *

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
    Comprueba el ge6er de conexión, si decuelve el tipo y la conexión
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
