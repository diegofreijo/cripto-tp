
def PotMod(a, b, n):
  a2p = a%n
  a = 1
  while b > 0:
    if b&1 > 0:
      a = (a * a2p) % n
    b = b>>1
    a2p = (a2p*a2p) % n
  return a
