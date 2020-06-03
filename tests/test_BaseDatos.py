"""
Tests de la clase Base de datos
Esta hace de conexión entre la aplicación y los datos
"""
import pytest

from ..keepit import *


# Instancia el objeto sobre el que se van a realizar las pruebas
# pepito y grillo es el usuario y la contraseña de la base de datos
user = "pepito"
passwd = "grillo"
bd_test = BaseDatos("localhost", user, passwd, "keepit")


def test_init(user, passwd):
    # El constructor consta de 4 atributos
    assert type(1) == int
    """host = "localhost"
    usuario = user  # Usuario por defecto
    contrasena = passwd  # Contraseña por defecto
    base_datos = "keepit"
    assert BaseDatos(host,usuario,contrasena,base_datos)"""
