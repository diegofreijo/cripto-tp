# -*- coding: cp1252 -*-
#
# LogicaRedParam.py
#
# Parametros (constantes?) utilizados en la Logica de Red
#
# 20071218 Matías Albanesi Cáceres
#
import struct

PRIMO_MINIMO = 1L<<33 # minimo valor permitido para el primo P recibido

MENSAJE_SOY_MANO = 'SOY_MANO'
MENSAJE_SOS_MANO = 'SOS_MANO'

# Longitudes
CANT_BITS_K = 128 # Clave usada en AES
CANT_BITS_PRIMOS = 256 # Tamaño de los primos generados
CANT_BITS_TS = 32 # Tamaño del timestamp / numero de secuencia enviado en cada paquete
CANT_CHARS_COMANDO = 1 # Tamaño en caracteres del comando enviado en cada paquete del juego al contrincante 
CANT_BITS_CARTAS = 160 # Tamaño de las codificacione de las cartas
#CANT_BITS_CARTAS_FIRMADAS           = CANT_BITS_PRIMOS    # Tamaño de las firmas de las cartas
#CANT_CHARS_CARTAS_FIRMADAS          = CANT_BITS_CARTAS_FIRMADAS / 8 # Tamaño en caracteresde las firmas de las cartas (supongo que eñ tamaño en bits es potencia de 2)
CANT_CHARS_LONGITUDES = 4 # Longitud en caracteres de los campos que dan la longitud del campo siguiente en un paquete
CANT_CHARS_TANTO = 2 # Tamaño en caracteres de los tantos cantados


# Comandos
COMANDO_QUIERO_ENVIDO       = 'a'
COMANDO_NO_QUIERO_ENVIDO    = 'b'
COMANDO_ENVIDO              = 'c'
COMANDO_ENVIDO_ENVIDO       = 'd'
COMANDO_REAL_ENVIDO         = 'e'
COMANDO_FALTA_ENVIDO        = 'f'
COMANDO_QUIERO_TRUCO        = 'g'
COMANDO_NO_QUIERO_TRUCO     = 'h'
COMANDO_TRUCO               = 'i'
COMANDO_RETRUCO             = 'j'
COMANDO_VALE_CUATRO         = 'k'
COMANDO_JUEGO_CARTA         = 'l'
COMANDO_CANTO_TANTO         = 'm'
COMANDO_SON_BUENAS          = 'n'
COMANDO_ME_VOY_AL_MAZO      = 'o'
COMANDO_GANE                = 'p'
COMANDO_PERDI               = 'q'
