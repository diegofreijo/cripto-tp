import struct
from LogicaRedStruct import *
from LogicaRedParam import *

class JugadaPaquete:
  #ts = None
  comando = None
  carta = None
  tanto = None
  def __init__(self, comando, carta, tanto):
    self.comando = comando
    self.carta = carta
    self.tanto = tanto

  def empaquetar(self):
    paquete = self.comando
    
    # Si hay carta, la agrego
    if self.carta != None:
      carta_str = long_to_infint(self.carta)
      # Agrego la longitud de la carta y luego a ella
      paquete = paquete + struct.pack('L', len(carta_str)) + carta_str
    # Si hay tanto, lo agrego
    elif self.tanto != None:
      tanto_str = str(self.tanto).zfill(CANT_CHARS_TANTO)
      paquete = paquete + tanto_str

    
    return paquete
  
  
  