import sys
sys.path.append("..\\..\\src\\red")
import Red

puerto = 65301

def server():
  f = open("c:\\EjemploPingServer.py.log", "w")
  Red.ActivarRegistro(f)
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
  f.close()

server()
