import sys
sys.path.append("..\\..\\src\\red")
import Red

puerto = 65301

if True:
  import time
  mi_sleep=time.sleep

def client():
  f = open("c:\\EjemploPingClient.py.log", "w")
  Red.ActivarRegistro(f)
  #s.setblocking(False)
  #s.connect(addr)
  Red.AbrirConexion('localhost', puerto)
  for i in 'a', 'b', 'z':
    print '[cli] voy a enviar %c' % i
    #while True:
    #  a = s.recv(1)
    #  if a == None or a == '': break
    #  print '[cli] recv', a
    print '[cli] enviando %c'%i
    #s.send(i)
    Red.Enviar(i)
    #e32.ao_sleep(0.5)
  print '[cli] fin envio'
  while True:
    #a = s.recv(1)
    a = Red.Recibir(1)
    if a == None or a == '': break
    print '[cli] recv', a
  print 'sleep(0.5)'
  mi_sleep(0.5)
  #while True:
  #  a = s.recv(100)
  #  if a == None or a == '': break
  #  print '[cli] recv', a
  #s.close()
  Red.CerrarConexion()
  print '[cli] ok. cliente desconectado'
  Red.ActivarRegistro(None)
  mi_sleep(0.5)

client()
