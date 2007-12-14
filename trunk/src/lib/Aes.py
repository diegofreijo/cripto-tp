from Crypto.Cipher import AES

def AesEncriptar(plain, key):
	aes = AES.new(key)
	return aes.encrypt(plain)
	
def AesDesencriptar(cypher, key):
	aes = AES.new(key)
	return aes.decrypt(cypher)
