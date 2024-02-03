import hashlib
import random


# Paso 1:
g = 2
p_hex = "B10B8F96A080E01DDE92DE5EAE5D54EC52C99FBCFB06A3C69A6A9DCA52D23B616073E28675A23D189838EF1E2EE652C013ECB4AEA906112324975C3CD49B83BFACCBDD7D90C4BD7098488E9C219A73724EFFD6FAE5644738FAA31A4FF55BCCC0A151AF5F0DC8B4BD45BF37DF365C1A65E68CFDA76D4DA708DF1FB2BC2E4A4371"

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




