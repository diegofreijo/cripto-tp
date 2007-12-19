execfile(r'D:\mac@sion.com\Cripto-TP\setpath.py')
import Red
import Registro

from EjemploChatServer import chatear

direcc = '127.0.0.1'
puerto = 65302

def client():
  logger = Registro.newRegistro("D:\\mac@sion.com\\EjemploChatClient.py.log")
  Red.ActivarRegistro(logger)
  Red.AbrirConexion(direcc, puerto)
  logger.info("[cli] Conectado")
  chatear("client", True) # ser el primero en hablar
  logger.info("[cli] Terminado")
  Red.ActivarRegistro(None)
  Red.CerrarConexion()
  logger.setArchivo(None)

if __name__ == "__main__":
  client()
