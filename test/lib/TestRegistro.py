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
execfile(r'D:\mac@sion.com\Cripto-TP\setpath.py')
import Registro

log = Registro.newRegistro()
log.setConsola(True)
log.setNivelConsola(Registro.DEBUG)
log.setArchivo("D:\\mac@sion.com\\log.log")
log.setNivelArchivo(Registro.INFO)
log.debug("solo por pantalla")
log.info("pantalla y archivo")
log.error("grave que sale por pantalla y archivo")
