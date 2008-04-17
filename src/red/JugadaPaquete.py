import struct
import Rsa
from LogicaRedStruct import *
from LogicaRedParam import *

class JugadaPaquete:
  sec = None
  comando = None
  carta = None
  tanto = None
  def __init__(self, sec, comando, carta, tanto):
    self.sec = sec
    self.comando = comando
    self.carta = carta
    self.tanto = tanto
    
  
  # Empaqueta, firma y agrega la longitud total del paquete
  def empaquetar(self, d, n):
    # Meto el numero de secuencia
    paquete = long_to_infint(self.sec).zfill(CANT_CHARS_SECUENCIA)
    
    # Meto el comando
    paquete = paquete + self.comando
    
    # Si hay carta, la meto
    if self.carta != None:
      carta_str = long_to_infint(self.carta)
      # Agrego la longitud de la carta y luego a ella
      paquete = paquete + struct.pack('L', len(carta_str)) + carta_str
      
    # Si hay tanto, lo meto
    elif self.tanto != None:
      tanto_str = str(self.tanto).zfill(CANT_CHARS_TANTO)
      paquete = paquete + tanto_str

    # Encripto el paquete y le agrego la longitud total
    paquete = Rsa.EncriptarTexto(paquete, d, n)
    longitud = struct.pack('L', len(paquete)).zfill(CANT_CHARS_LONGITUDES)
    paquete = longitud + paquete
    
    return paquete
  
  
  