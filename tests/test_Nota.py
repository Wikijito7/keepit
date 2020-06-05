"""
Tests de la Clase Nota
"""
import pytest
from keepit import *

# Instancio la nota ya que es la que se va ha utilizar para los test
usuario_test = Usuario("test@test.es", "Amapola")
nota_Test = Nota("Matrícula", "Entrega solicitud dentro de plazo", "1ºDAW", usuario_test, "1", ["colegio", ])


def test_get_etiquetas():
    """
    Comprueba que devuelve la o las etiquetas de una nota
    :return list: lista de las etiquetas
    """
    assert nota_Test.get_etiquetas() == ['colegio']


def test_get_categoria():
    """
    Comrpueba que devuelve la categoría
    :return str: string de la categoría
    """
    assert nota_Test.get_categoria() == '1ºDAW'


def test_get_titulo():
    """
    Comprueba que devuelve el título de la nota
    :return str: String del titulo
    """
    assert nota_Test.get_titulo() == 'Matrícula'


def test_get_contenido():
    """
    Comprueba que devuelve el contenido de la nota
    :return str: String del contenido de la nota
    """
    assert nota_Test.get_contenido() == 'Entrega solicitud dentro de plazo'


def test_get_as_list():
    """
    Comprueba que devuelve id, titulo, categoría y email de la nota
    :return list: id, titulo ,categoría, email  de la nota
    """
    assert nota_Test.get_as_list() == ['1', 'Matrícula', '1ºDAW', 'test@test.es']


def test_get_etiquetas_str():
    """
    Comprueba que devuelve la etiqueta en formato str en lugar de string
    :return str: String de las etiquetas
    """
    assert nota_Test.get_etiquetas_str() == 'colegio'


def test_set_etiquetas():
    """
    Sustituye las etiquetas en la nota
    :return void:
    """
    # Comprobamos las etiquetas o etiqueta antes de cambiar
    assert nota_Test.get_etiquetas() == ['colegio']

    # Introduzco nuevas etiquetas
    nota_Test.set_etiquetas(['instituto', 'Alberti', 'secretaria'])
    assert nota_Test.get_etiquetas() == ['instituto', 'Alberti', 'secretaria']


def test_add_etiqueta():
    """
    Añade nuevas etiquetas a las ya existentes en la nota
    :return void:
    """
    # Comprobamos las etiquetas antes de agregar nuevas
    nota_Test.set_etiquetas(['instituto', 'Alberti', 'secretaria'])
    assert nota_Test.get_etiquetas() == ['instituto', 'Alberti', 'secretaria']

    # Agregamos nuevas a las existentes
    nota_Test.add_etiqueta('carro')
    nota_Test.add_etiqueta('bicicleta')

    # Comprobamos que efectivamente se han introducido las nuecas etiquetas
    assert nota_Test.get_etiquetas() == ['instituto', 'Alberti', 'secretaria', 'carro', 'bicicleta']


def test_set_categoria():
    """
    Comprueba que se sustituye la categoría
    :return void:
    """
    # Comprobamos la categoría antes de actualizar
    assert nota_Test.get_categoria() == '1ºDAW'

    # Actualizamos la categoría
    nota_Test.set_categoria('2ºDAW')

    # Comprobamos que la categoría se ha actualizado correctamente
    assert nota_Test.get_categoria() == '2ºDAW'


def test_set_titulo():
    """
    Comprueba si se actualiza el titulo de la nota
    :return str:
    """
    # Comprobamos la categoría antes de actualizar
    assert nota_Test.get_titulo() == 'Matrícula'

    # Actualizamos el titulo
    nota_Test.set_titulo('Matriculaciones')

    # Comprobamos que se ha actualizado correctamente
    assert nota_Test.get_titulo() == 'Matriculaciones'


def test_set_contenido():
    """
    Comprueba si se actualiza el titulo de la nota
    :return void:
    """
    # Comprueba el contenido
    assert nota_Test.get_contenido() == 'Entrega solicitud dentro de plazo'

    # Actualizo contenido
    nota_Test.set_contenido('El plazo finaliza el 15 de septiembre')

    # Compruebo que se actualiza el contenido correctamente
    assert nota_Test.get_contenido() == 'El plazo finaliza el 15 de septiembre'


def test_str_nota():
    """
    Comprueba si se devuelve la nota completa en formato str
    :return str: String del contenido completo de la nota
    """
    assert nota_Test.__str__() == "Nota(titulo: 'Matriculaciones', categoría: '2ºDAW', contenido: 'El plazo finaliza el 15 de septiembre', usuario: 'Usuario('email':test@test.es', 'password':'Amapola')', identificador: '1', etiquetas: '['instituto', 'Alberti', 'secretaria', 'carro', 'bicicleta']')"
