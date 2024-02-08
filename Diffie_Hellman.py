import hashlib
import random


# Paso 1:
g = 2
p_hex = "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA237327FFFFFFFFFFFFFFFF"

# Convertir el número hexadecimal a entero
p = int(p_hex, 16)

print("Número primo de Diffie - Hellman: < ", p, ">")

# Paso 2:
a_llave_privada = random.getrandbits(256)
b_llave_privada = random.getrandbits(256)

print("Llave privada de Alice: < ", a_llave_privada, ">")
print("Llave privada de Bob: < ", b_llave_privada, ">")

# Paso 3:
a_llave_publica = pow(g, a_llave_privada, p)
b_llave_publica = pow(g, b_llave_privada, p)

print("Llave publica de Alice: < ", a_llave_publica, ">")
print("Llave publica de Bob: < ", b_llave_publica, ">")

# Paso 4.1:
s_alice = pow(b_llave_publica, a_llave_privada, p)
s_bob = pow(a_llave_publica, b_llave_privada, p)

print("Llave compartida de Alice: < ", s_alice, ">")
print("Llave compartida de Bob: < ", s_bob, ">")

# Paso 4.2:

hash_s_Alice = hashlib.sha256(str(s_alice).encode()).hexdigest()
hash_s_Bob = hashlib.sha256(str(s_bob).encode()).hexdigest()

if hash_s_Alice == hash_s_Bob:
    print("Las claves secretas son iguales y válidas.")
    print("Clave secreta generada:", hash_s_Alice)
else:
    print("Las claves secretas no coinciden.")




