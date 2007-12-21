import socket
import sys
import Registro

sock = None
dirRemota = None

prefijo = '[' + __name__ + '] ' # nombre del modulo
logger = Registro.newRegistro()
DEBUGLOG=lambda x: logger.debug(x)

def activarRegistro(nuevoLogger):
    global logger, DEBUGLOG
    if logger != None:
        logger.debug(prefijo + "Fin del registro")
        logger.setArchivo(None)
        logger = nuevoLogger
    if logger == None:
        DEBUGLOG=lambda x: 0
    else:
        DEBUGLOG=lambda x: logger.debug(x)
    DEBUGLOG(prefijo + "Comienzo del registro")


def esperarConexion(ip, puerto):
    global sock, dirRemota
    pf = prefijo + '[esperarConexion()] '
    DEBUGLOG(pf + "esperarConexion(" + repr(ip) + ", " + repr(puerto)+")")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if (ip == None or ip == ''):
        ip = '127.0.0.1'
    DEBUGLOG(pf + "bind((" + repr(ip) + ", " + repr(puerto)+"))")
    s.bind((ip, puerto))
    DEBUGLOG(pf + "listen(1)")
    s.listen(1)
    DEBUGLOG(pf + "accept()")
    (sock, dirRemota) = s.accept()
    DEBUGLOG(pf + "(" + str(sock) + ", " + str(dirRemota) + ") = accept()")


def abrirConexion(ip, puerto):
    global sock, dirRemota
    pf = prefijo + '[abrirConexion()] '
    DEBUGLOG(pf + "abrirConexion(" + str(ip) + ", " + str(puerto)+")")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = (ip, puerto)
    DEBUGLOG(pf + "conectando a "+str(addr)+"...")
    s.connect(addr)
    sock = s
    dirRemota = addr
    DEBUGLOG(pf + "conectado")


def cerrarConexion():
    pf = prefijo + '[cerrarConexion()] '
    DEBUGLOG(pf + "cerrarConexion()")
    sock.close()
    DEBUGLOG(pf + "conexion cerrada")


def enviar(datos):
    pf = prefijo + '[enviar()] '
    DEBUGLOG(pf + "enviar(\"" + repr(datos)+"\")")
    sock.send(datos)
    DEBUGLOG(pf + "datos enviados")


def recibir(longitud):
    pf = prefijo + '[recibir()] '
    DEBUGLOG(pf + "recibir(" + str(longitud)+")")
    recibido = ''
    while len(recibido) < longitud:
        try:
            rv = sock.recv(longitud - len(recibido))
            DEBUGLOG(pf + "datos recibidos: \"" + repr(rv) + "\"");
        except socket.error, e:
            DEBUGLOG(pf + "excepcion: \"" + repr(e) + "\"");
            rv = ''
        recibido = recibido + rv
        if rv == '': break
    #
    return recibido

