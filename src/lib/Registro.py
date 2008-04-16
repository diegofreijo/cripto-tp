# -*- coding: cp1252 -*-
#
# Registro.py
#
# Matías Albanesi Cáceres, 20071217
#
# Uso:
# from Registro import *
# log = Registro()
# log.setConsola(True)
# log.setNivelConsola(DEBUG)
# log.setArchivo("C:\\log.log")
# log.setNivelArchivo(INFO)
# log.debug("solo por pantalla")
# log.info("pantalla y archivo")
# log.error("grave que sale por pantalla y archivo")
#

DEBUG = 0
INFO = 1
WARN = 2
ERROR = 3
NONE = 4

class Registro:

  def __init__(self, archivo = None):
    self.archivo = None
    self.of = None
    self.nivelArchivo = DEBUG
    self.consola = False
    self.nivelConsola = DEBUG
    self.setConsola(False)
    self.setNivelConsola(DEBUG)
    self.setArchivo(archivo)
    self.setNivelArchivo(DEBUG)

  def setConsola(self, activado):
    self.consola = activado

  def setNivelConsola(self, nivel = NONE):
    if nivel >= DEBUG and nivel <= NONE:
      self.nivelConsola = nivel

  def setArchivo(self, archivo):
    if self.of != None:
      # cerrar salida al archivo abierto
      self.of.close()
      self.of = None
    #
    self.archivo = archivo
    if archivo != None:
      try:
        self.of = open(archivo, "w")
      except:
        self.of = None
        self.archivo = None
        return False

  def setNivelArchivo(self, nivel = NONE):
    if nivel >= DEBUG and nivel <= NONE:
      self.nivelArchivo = nivel

  def _loguear(self, nivel, mensaje, nueva_linea = True):
    if self.of != None:
      if self.nivelArchivo <= nivel:
        self.of.write(mensaje + '\n')
    if self.consola:
      if self.nivelConsola <= nivel:
        if nueva_linea:
          print mensaje
        else:
          print mensaje,
    if self.of != None:
      if self.nivelArchivo <= nivel:
        self.of.flush()

  def debug(self, mensaje):
    self._loguear(DEBUG, mensaje)

  def info(self, mensaje, nueva_linea = True):
    self._loguear(INFO, mensaje, nueva_linea)

  def warn(self, mensaje):
    self._loguear(WARN, mensaje)

  def error(self, mensaje):
    self._loguear(ERROR, mensaje)

def newRegistro(archivo = None):
  return Registro(archivo)
