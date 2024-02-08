import hashlib
import random

# Paso 1:
g = 2
p_hex = "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA237327FFFFFFFFFFFFFFFF"

# Convertir el número hexadecimal a entero
p = int(p_hex, 16)
print("\nNúmero primo de Diffie-Hellman: ", p)
print("")

# Llaves privadas de Alice, Bob e Eve
llave_privada_alice = random.getrandbits(256)
llave_privada_bob = random.getrandbits(256)
llave_privada_eve = random.getrandbits(256)

print("Llave privada de Alice: ", llave_privada_alice)
print("Llave privada de Bob: ", llave_privada_bob)
print("Llave privada de Eve: ", llave_privada_eve)
print("")

# Llaves públicas de Alice, Bob e Eve
mensaje_alice = pow(g, llave_privada_alice, p)
mensaje_bob = pow(g, llave_privada_bob, p)
mensaje_eve = pow(g,llave_privada_eve, p)


print("Llave pública de Alice: ", mensaje_alice)
print("Llave pública de Bob: ", mensaje_bob)

print("")


# Cálculo de las llaves secretas entre Alice y Eve y Bob y Eve
interferencia_eve_alice = pow(mensaje_alice, llave_privada_eve, p)
interferencia_alice_eve = pow(mensaje_eve, llave_privada_alice, p)
interferencia_eve_bob = pow(mensaje_bob, llave_privada_eve, p)
interferencia_bob_eve = pow(mensaje_eve, llave_privada_bob, p)

print("Llave secreta de Alice (calculada por Eve): ", interferencia_eve_alice)
print("Llave secreta de Eve (calculada por Alice): ", interferencia_alice_eve)
print("Llave secreta de Bob (calculada por Eve): ", interferencia_eve_bob)
print("Llave secreta de Eve (calculada por Bob): ", interferencia_bob_eve)
print("")

hash_interferencia_eve_alice = hashlib.sha256(str(interferencia_eve_alice).encode()).hexdigest()
hash_interferencia_alice_eve = hashlib.sha256(str(interferencia_alice_eve).encode()).hexdigest()
hash_interferencia_eve_bob = hashlib.sha256(str(interferencia_eve_bob).encode()).hexdigest()
hash_interferencia_bob_eve = hashlib.sha256(str(interferencia_bob_eve).encode()).hexdigest()

print("Hash de la llave secreta de Alice (calculada por Eve): ", hash_interferencia_eve_alice)
print("Hash de la llave secreta de Eve (calculada por Alice): ", hash_interferencia_alice_eve)
print("Hash de la llave secreta de Bob (calculada por Eve): ", hash_interferencia_eve_bob)
print("Hash de la llave secreta de Eve (calculada por Bob): ", hash_interferencia_bob_eve)
print("")

# Verificar si las llaves secretas entre Alice y Eve y Bob y Eve son iguales
if hash_interferencia_eve_bob == hash_interferencia_bob_eve and hash_interferencia_alice_eve == hash_interferencia_eve_alice:
    print("¡Ataque MITM exitoso!")
    print("Llave secreta obtenida :", hash_interferencia_eve_alice)
else:
    print("Error: Las llaves secretas no coinciden.")
