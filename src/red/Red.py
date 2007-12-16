import socket

sock = None
dirRemota = None

#DEBUGLOG=lambda x: sys.stdout.write(x+"\n")
DEBUGLOG=lambda x: 0
oflog = None

def _debugLog(x):
	global oflog
	if oflog != None: oflog.write(x+"\n")
	print x
	if oflog != None: oflog.flush()

def ActivarRegistro(destino):
	global oflog, DEBUGLOG
	if oflog != None: DEBUGLOG("Fin del registro de Red.py")
	oflog = destino
	if destino == None:
		DEBUGLOG=lambda x: 0
	else:
		DEBUGLOG=lambda x: _debugLog(x)
	DEBUGLOG("Comienzo del registro de Red.py")


def EsperarConexion(ip, puerto):
	global sock, dirRemota
	DEBUGLOG("[ec] EsperarConexion(" + str(ip) + ", " + str(puerto)+")")
	#raise "No implementado"
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	if (ip == None or ip == ''):
		ip = 'localhost'
	DEBUGLOG("[ec] bind((" + str(ip) + ", " + str(puerto)+"))")
	s.bind((ip, puerto))
	DEBUGLOG("[ec] listen(1)")
	s.listen(1)
	DEBUGLOG("[ec] accept()")
	(sock, dirRemota) = s.accept()
	DEBUGLOG("[ec] (" + str(sock) + ", " + str(dirRemota) + ") = accept()")


def AbrirConexion(ip, puerto):
	global sock, dirRemota
	DEBUGLOG("[ac] AbrirConexion(" + str(ip) + ", " + str(puerto)+")")
	#raise "No implementado"
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	addr = (ip, puerto)
	DEBUGLOG("[ac] conectando a "+str(addr)+"...")
	s.connect(addr)
	sock = s
	dirRemota = addr
	DEBUGLOG("[ac] conectado")


def CerrarConexion():
	#raise "No implementado"
	DEBUGLOG("[cc] CerrarConexion()")
	sock.close()
	DEBUGLOG("[cc] conexion cerrada")


def Enviar(datos):
	#raise "No implementado"
	DEBUGLOG("[en] Enviar(\"" + repr(datos)+"\")")
	sock.send(datos)
	DEBUGLOG("[en] datos enviados")

	
def Recibir(longitud):
	#raise "No implementado"
	DEBUGLOG("[re] Recibir(" + str(longitud)+")")
	try:
		rv = sock.recv(longitud)
		DEBUGLOG("[re] datos recibidos: \"" + rv + "\"");
	except socket.error, e:
		DEBUGLOG("[re] excepcion: \"" + repr(e) + "\"");
		rv = None
	return rv
