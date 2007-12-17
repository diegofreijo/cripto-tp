import sys
sys.path.append("..\\..\\src\\red")
import Red
from EjemploChatServer import chatear

puerto = 65302

def client():
  f = open("c:\\EjemploChatClient.py.log", "w")
  Red.ActivarRegistro(f)
  Red.AbrirConexion('localhost', puerto)
  print "[cli] Conectado"
  chatear("client", True) # ser el primero en hablar
  print "[cli] Terminado"
  Red.ActivarRegistro(None)
  Red.CerrarConexion()
  f.close

if __name__ == "__main__":
  client()
