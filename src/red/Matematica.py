
def EuclidesExtendido(a,b):
	if b == 0:
		return [a,1,0]
	else:
		ee = EuclidesExtendido(b, a % b)
		return [ee[0], ee[2], ee[1] - (int)(a / b) * ee[2]]


def int2bin(n):
	if n < 0:  raise ValueError, "n: " + str(n)
	if n == 0: return "0"
	ret = ""
	while n > 0:
		ret = str(n % 2) + ret
		n = n >> 1
	return ret
	
