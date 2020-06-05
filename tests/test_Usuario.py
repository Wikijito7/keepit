"""
Tests de la calse Usuario. Esta simplemente se utiliza para logear registrar usuarios
las notas quedan registradas al email de estos usuario
"""
import pytest
from keepit import Usuario

usuario_test = Usuario("test@test.es", "amapola")


def test_init():
    """
    Comprueba el constructor y atributos
    """
    # Constructor
    assert Usuario("test@test.es", "amapola")

    # Atributo email
    assert Usuario("test@test.es", "amapola").email == "test@test.es"
    assert type(Usuario("test@test.es", "amapola").email) == str

    # Atributo password
    assert Usuario("test@test.es", "amapola").password == "amapola"
    assert type(Usuario("test@test.es", "amapola").password) == str


def test_get_email():
    """
    Comprueba que se devuelve el email del usuario
    :return str: email del usuario
    """
    assert usuario_test.get_email() == "test@test.es"


def test_str_Usuario():
    """
    Comrpueba que devuelve en formato str el usuario completo
    :return str:  String del usuario completo
    """
    assert usuario_test.__str__() == "Usuario('email':test@test.es', 'password':'amapola')"
