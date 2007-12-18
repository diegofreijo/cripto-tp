import sys
sys.path.append("..\\..\\src\\lib")
sys.path.append("..\\..\\src\\red")
import Red
import Registro

from EjemploChatServer import chatear

puerto = 65302

def client():
  logger = Registro.newRegistro("D:\\FCEN\\EjemploChatClient.py.log")
  Red.ActivarRegistro(logger)
  Red.AbrirConexion('localhost', puerto)
  print "[cli] Conectado"
  chatear("client", True) # ser el primero en hablar
  print "[cli] Terminado"
  Red.ActivarRegistro(None)
  Red.CerrarConexion()
  logger.setArchivo(None)

if __name__ == "__main__":
  client()
