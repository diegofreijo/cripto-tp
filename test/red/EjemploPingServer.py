execfile(r'D:\mac@sion.com\Cripto-TP\setpath.py')
import Red
import Registro

puerto = 65301

def server():
  logger = Registro.newRegistro("D:\\mac@sion.com\\EjemploPingServer.py.log")
  Red.ActivarRegistro(logger)
  Red.EsperarConexion('localhost', puerto)
  print "[serv] Conectado"
  while 1:
    try:
      a = Red.Recibir(1)
      if a == None or a == '': break
    except socket.error:
      break
    print '[serv] eco', a
    Red.Enviar(a)
  #
  Red.ActivarRegistro(None)
  Red.CerrarConexion()
  logger.setArchivo(None)

server()
