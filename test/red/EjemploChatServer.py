import sys
sys.path.append("..\\..\\src\\lib")
sys.path.append("..\\..\\src\\red")
import struct
import Red
import Registro

puerto = 65302

def server():
  logger = Registro.newRegistro("D:\\FCEN\\EjemploChatServer.py.log")
  Red.ActivarRegistro(logger)
  Red.EsperarConexion('localhost', puerto)
  print "[serv] Conectado"
  chatear("server", False) # esperar a que el otro hable
  print "[serv] Terminado"
  Red.ActivarRegistro(None)
  Red.CerrarConexion()
  logger.setArchivo(None)


def obt_texto(mensaje, val = None):
  while True:
    try:
      texto=raw_input(mensaje)
    except EOFError:
      print 'EOFError'
      texto=''
    # Si hay una validacion, ejecutarla
    if val == None: break
    if val(texto): break
  return texto


def chatear(identificacion, miTurno):
  """
  Asumiendo que hay una conexion abierta en el modulo Red.py, utilizarla para enviar y recibir mensajes
  por turnos.
  """
  while True:
    if miTurno:
      # pedir por consola un mensaje y enviarlo
      msg = obt_texto(identificacion + ": ")
      # enviar long. mensaje en 4 bytes
      Red.Enviar(struct.pack('L', len(msg))) # 'L' es unsigned long
      # enviar el mensaje
      Red.Enviar(msg)
      if msg.lower() == '/quit':
        break
    else:
      # esperar un mensaje del otro extremo y mostrarlo por pantalla
      t = Red.Recibir(4) # 4 bytes por el unsigned long
      if t == None:
        print 'El otro extremo termino la conexion'
        break
      u = struct.unpack('L', t)
      msg = Red.Recibir(u[0]) # mensaje a recibir
      if msg == None:
        print 'El otro extremo termino la conexion'
        break
      print 'Respuesta: ' + msg
      if msg.lower() == '/quit':
        break
    #
    miTurno = not miTurno
  #

if __name__ == "__main__":
  server()
