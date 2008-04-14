import struct
from LogicaRedStruct import *

class JugadaPaquete:
  ts = None
  comando = None
  carta = None
  tanto = None
  def __init__(self, comando, carta):
    self.comando = comando
    self.carta = carta

  def empaquetar(self):
    paquete = self.comando
    
    # Si hay carta, la agrego
    if self.carta != None:
      carta_str = long_to_infint(self.carta)
      # Agrego la longitud de la carta y luego a ella
      paquete = paquete + struct.pack('L', len(carta_str)) + carta_str
    
    return paquete
  
  
  