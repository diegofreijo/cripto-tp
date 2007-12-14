import sys
sys.path.append("")
import Rsa
from math import log

## Leo las opciones de consola
plain = sys.argv[1]
tam_primos = int(sys.argv[2])

[n, e, d] = Rsa.GenerarClaves(tam_primos)

cypher = Rsa.EncriptarTexto(plain, e, n)
plain_rearmado = Rsa.DesencriptarTexto(cypher, d, n)

print "n = " + str(n) + "	tam_n: " + str(int(log(n,2)) + 1)
print "e = " + str(e) + "		d = " + str(d)

print "plain = '" + plain + "'"
print "cypher = " + str(cypher)
print "plain_rearmado: '" + plain_rearmado + "'"
