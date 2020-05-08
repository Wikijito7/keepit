import pymysql
from tkinter import *

# kipi
class BaseDatos: 
    def __init__(self, host, user, passw, nombre_bd):
        self.conexion =  pymysql.connect(host, user, passw, nombre_bd)
        self.cursor = self.conexion.cursor()

    def get_conexion(self):
        return self.conexion

    def select(self, tabla): # bd.select("Categorias") -> lista con todas las categorias (select * from tabla)
        pass

    def select_filtrado(self, tabla, parametros): # lista con lo filtrado (select * from tabla where parametro)
        pass
        
    def insert(self, tabla):
        pass
        

class Nota:
    def __init__(self, titulo, contenido, categoria, usuario, identificador, etiquetas = None):
        if isinstance(titulo, str) and isinstance(categoria, str) and isinstance(contenido, str) and isinstance(usuario, Usuario):
            self.titulo = titulo
            self.categoria = categoria # ""
            self.contenido = contenido
            self.usuario = usuario
            self.identificador = identificador
            if etiquetas == None:
                self.etiquetas = [] # []
            elif isinstance(etiquetas, list):
                self.etiquetas = etiquetas
            else:
                raise ValueError("Las etiquetas deben venir dadas con una lista.")
        else:
            raise ValueError

    #getter and setters for Nota
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
    bd = BaseDatos("localhost", "keepit", "Antoniojose@10", "keepit") #host, user, passw, nombre_bd 
    bd.cursor.execute("select * from Categorias")
    print(bd.cursor.rowcount)
    bd.get_conexion().commit()
    