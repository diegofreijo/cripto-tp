import socket
import sys
import Registro

sock = None
dirRemota = None

logger = None
DEBUGLOG=lambda x: 0

def ActivarRegistro(nuevoLogger):
	global logger, DEBUGLOG
	if logger != None:
                DEBUGLOG("[Red.py] Fin del registro")
                logger.setArchivo(None)
        logger = nuevoLogger
	if logger == None:
		DEBUGLOG=lambda x: 0
	else:
		DEBUGLOG=lambda x: logger.debug(x)
	DEBUGLOG("[Red.py] Comienzo del registro")


def EsperarConexion(ip, puerto):
	global sock, dirRemota
	DEBUGLOG("[Red.py] EsperarConexion(" + str(ip) + ", " + str(puerto)+")")
	#raise "No implementado"
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	if (ip == None or ip == ''):
		ip = 'localhost'
	DEBUGLOG("[Red.py - ec] bind((" + str(ip) + ", " + str(puerto)+"))")
	s.bind((ip, puerto))
	DEBUGLOG("[Red.py - ec] listen(1)")
	s.listen(1)
	DEBUGLOG("[Red.py - ec] accept()")
	(sock, dirRemota) = s.accept()
	DEBUGLOG("[Red.py - ec] (" + str(sock) + ", " + str(dirRemota) + ") = accept()")


def AbrirConexion(ip, puerto):
	global sock, dirRemota
	DEBUGLOG("[Red.py] AbrirConexion(" + str(ip) + ", " + str(puerto)+")")
	#raise "No implementado"
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	addr = (ip, puerto)
	DEBUGLOG("[Red.py - ac] conectando a "+str(addr)+"...")
	s.connect(addr)
	sock = s
	dirRemota = addr
	DEBUGLOG("[Red.py - ac] conectado")


def CerrarConexion():
	#raise "No implementado"
	DEBUGLOG("[Red.py] CerrarConexion()")
	sock.close()
	DEBUGLOG("[Red.py - cc] conexion cerrada")


def Enviar(datos):
	#raise "No implementado"
	DEBUGLOG("[Red.py] Enviar(\"" + repr(datos)+"\")")
	sock.send(datos)
	DEBUGLOG("[Red.py - en] datos enviados")

	
def Recibir(longitud):
	#raise "No implementado"
	DEBUGLOG("[Red.py] Recibir(" + str(longitud)+")")
	try:
		rv = sock.recv(longitud)
		DEBUGLOG("[Red.py - re] datos recibidos: \"" + rv + "\"");
	except socket.error, e:
		DEBUGLOG("[Red.py - re] excepcion: \"" + repr(e) + "\"");
		rv = None
	return rv
