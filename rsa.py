# import Crypto
# from Crypto.Util.number import long_to_bytes,bytes_to_long
# from Crypto import Random
#
#
#
# # Números de bits:
# bits = 1024
#
# # Obtener los primos para Alice:
# primo_alice = Crypto.Util.number.getPrime(bits, randfunc=Crypto.Random.get_random_bytes)
# q_alice = Crypto.Util.number.getPrime(bits, randfunc=Crypto.Random.get_random_bytes)
#
#
# print("Primo de Alice: ", primo_alice)
# print("Número Q de Alice: ", q_alice)
#
# # Obtener los primos para Bob:
# primo_bob = Crypto.Util.number.getPrime(bits, randfunc=Crypto.Random.get_random_bytes)
# q_bob = Crypto.Util.number.getPrime(bits, randfunc=Crypto.Random.get_random_bytes)
#
#
# print("Primo de Alice: ", primo_alice)
# print("Número Q de Alice: ", q_alice)
#
#
# # Obtenemos la primera parte de la llave pública de Alice y Bob:
# n_Alice = primo_alice*q_alice
# print(" Llave pública de Alice: ", n_Alice)
#
# n_Bob = primo_bob*q_bob
# print(" Llave pública de Bob: ", n_Bob)
#
#
# # Calculamos el Indicador de Euler phi:
# phi_Alice = (primo_alice-1)*(q_alice-1)
# print("Phi de Alice: ", phi_Alice)
#
# phi_Bob = (primo_bob-1)*(q_bob-1)
# print("Phi de Bob: ", phi_Bob)
#
#
# # Por razones de eficiencia, tomaremos el numero 4 de Fermat, que vale 65537, para el Indicador de Euler
# # ya que es un numero primo largo, que no es potencia de 2:
# e = 65537
#
#
# # Calular la llave privada de Alice:
# #d_Alice = pow(e, -1, phi_Alice)
# d_Alice = Crypto.Util.number.inverse(e, phi_Alice)
# print("Llave privada de Alice: ", d_Alice)
#
# # Calular la llave privada de Bob:
# #d_Bob = pow(e, -1, phi_Bob)
# d_Bob = Crypto.Util.number.inverse(e, phi_Bob)
# print("Llave privada de Bob: ", d_Bob)
#
#
# # Ciframos el mensaje:
# mensaje = "UYUYUYUYUY"
# print("Mensaje Original: ", mensaje)
# print("Longtud del mensaje en bytes: ", len(mensaje.encode("utf-8")))
#
#
# # Convertir el mensaje a núemro:
# mensaje_en_numero = int.from_bytes(bytes(mensaje.encode("utf-8")), "big")
# print("Mensaje convertido a número: ", mensaje_en_numero, "\n")
#
# # Ciframos el mensaje:
# mensaje_cifrado = pow(mensaje_en_numero, e, n_Bob)
# print("Mensaje cifrado: ", mensaje_cifrado)
#
#
# # Deciframos el mensaje:
# mensaje_descifrado = pow(mensaje_cifrado, d_Bob, n_Bob)
# print("Mensaje descifrado: ", mensaje_descifrado)
#
#
# # Convertimos el mensaje de número a texto:
# mensaje_final = int.to_bytes(mensaje_descifrado, len(mensaje), byteorder="big").decode("utf-8")
# print("Mensaje final en texto: ", mensaje_final, "\n")

#hash_mensaje = Crypto.Hash.SHA256.new(mensaje_final.encode("utf-8"))


import Crypto
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto import Random
from Crypto.Hash import SHA256

# Números de bits:
bits = 1024

# Obtener los primos para Alice:
primo_alice = Crypto.Util.number.getPrime(bits, randfunc=Crypto.Random.get_random_bytes)
q_alice = Crypto.Util.number.getPrime(bits, randfunc=Crypto.Random.get_random_bytes)

print("Primo de Alice: ", primo_alice)
print("Número Q de Alice: ", q_alice)

# Obtener los primos para Bob:
primo_bob = Crypto.Util.number.getPrime(bits, randfunc=Crypto.Random.get_random_bytes)
q_bob = Crypto.Util.number.getPrime(bits, randfunc=Crypto.Random.get_random_bytes)

print("Primo de Bob: ", primo_bob)
print("Número Q de Bob: ", q_bob)

# Obtenemos la primera parte de la llave pública de Alice y Bob:
n_Alice = primo_alice * q_alice
print("Llave pública de Alice: ", n_Alice)

n_Bob = primo_bob * q_bob
print("Llave pública de Bob: ", n_Bob)

# Calculamos el Indicador de Euler phi:
phi_Alice = (primo_alice - 1) * (q_alice - 1)
print("Phi de Alice: ", phi_Alice)

phi_Bob = (primo_bob - 1) * (q_bob - 1)
print("Phi de Bob: ", phi_Bob)

# Por razones de eficiencia, tomaremos el número 4 de Fermat, que vale 65537, para el Indicador de Euler
# ya que es un número primo largo, que no es potencia de 2:
e = 65537

# Calcular la llave privada de Alice:
d_Alice = Crypto.Util.number.inverse(e, phi_Alice)
print("Llave privada de Alice: ", d_Alice)

# Calcular la llave privada de Bob:
d_Bob = Crypto.Util.number.inverse(e, phi_Bob)
print("Llave privada de Bob: ", d_Bob)

# Ciframos el mensaje:
mensaje = "Hola Bob, soy Alice."
print("Mensaje Original: ", mensaje)
print("Longitud del mensaje en bytes: ", len(mensaje.encode("utf-8")))

# Convertir el mensaje a número:
hash_mensaje = SHA256.new(mensaje.encode("utf-8"))
mensaje_en_numero = bytes_to_long(hash_mensaje.digest())
print("Mensaje convertido a número: ", mensaje_en_numero, "\n")

# Ciframos el mensaje:
mensaje_cifrado = pow(mensaje_en_numero, d_Alice, n_Alice)
print("Mensaje cifrado: ", mensaje_cifrado)

# Alice firma el HASH h(M) con su llave privada
firma = pow(mensaje_en_numero, d_Alice, n_Alice)

# Bob recibe el mensaje firmado por Alice
# y con la llave pública de Alice verifica si el mensaje fue realmente firmado por Alice
verificacion = pow(firma, e, n_Alice)

print("Mensaje en numeros: ", mensaje_en_numero)
print("Verificación: ", verificacion)


# Verificar si los hash coinciden
if verificacion == mensaje_en_numero:
    print("El mensaje fue firmado correctamente por Alice.")
else:
    print("El mensaje no fue firmado correctamente por Alice.")
