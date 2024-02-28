import hashlib
import Crypto
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto import Random
from Crypto.Hash import SHA256
# Hacer un hash de una cadena de texto de 1050 caracteres,
cadena_1050_caracteres = """
En la vida, cada paso cuenta. Cada elección moldea nuestro camino. No temas equivocarte, pues en los errores también yace la sabiduría.
Levántate con determinación, aprende con humildad y avanza con valentía. El tiempo es un regalo preciado, úsalo con sabiduría. Cultiva tus sueños con pasión, nutre tus relaciones con amor y abraza cada desafío como una oportunidad de crecimiento.
Recuerda siempre tu valía, pues eres único e irrepetible. Vive con gratitud, brilla con autenticidad y nunca pierdas la esperanza.
Tu historia aún está siendo escrita, así que toma las riendas y haz de cada día una página memorable.
El mundo espera tu luz, así que no temas brillar.
Saber vivir es la mejor forma de aprender. Cada cosa que haces, es una oportunidad de crecer. 
12345678901234567890123456789012345678901234523767890123456789823901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
"""
print("||||||––––––-|||||||")
num_caracteres_con_espacios = len(cadena_1050_caracteres)
print("Longitud de la cadena de texto de 1050 caracteres:", num_caracteres_con_espacios)
print("||||||––––––-|||||||")


hash_1050_caracteres = SHA256.new(cadena_1050_caracteres.encode("utf-8"))
print("HASH de una cadena de texto de 1050 caracteres:", hash_1050_caracteres.hexdigest())
print("||||||––––––-|||||||")

# El mensaje original se divide en partes más pequeñas de 128 caracteres antes de ser cifrado y enviado
mensaje_dividido_128_caracteres = [cadena_1050_caracteres[i:i+128] for i in range(0, len(cadena_1050_caracteres), 128)]


print("|---------------------------|")
# Comprobamos que efectivamente se ha dividido el mensaje correctamente
print("El mensaje se divide en partes de 128 caracteres: ",mensaje_dividido_128_caracteres)
print("|---------------------------|")

# Preparamos las llaves para Alice y Bob
bits = 1024

# Obtener los primos para Alice:
primo_alice = Crypto.Util.number.getPrime(bits, randfunc=Crypto.Random.get_random_bytes)
q_alice = Crypto.Util.number.getPrime(bits, randfunc=Crypto.Random.get_random_bytes)

print("Primo de Alice: ", primo_alice)
print("|---------------------------|")
print("Número Q de Alice: ", q_alice)
print("|---------------------------|")

# Obtener los primos para Bob:
primo_bob = Crypto.Util.number.getPrime(bits, randfunc=Crypto.Random.get_random_bytes)
q_bob = Crypto.Util.number.getPrime(bits, randfunc=Crypto.Random.get_random_bytes)

print("Primo de Bob: ", primo_bob)
print("|---------------------------|")
print("Número Q de Bob: ", q_bob)
print("|---------------------------|")

# Obtenemos la primera parte de la llave pública de Alice y Bob:
n_Alice = primo_alice * q_alice
print("Llave pública de Alice: ", n_Alice)
print("|---------------------------|")

n_Bob = primo_bob * q_bob
print("Llave pública de Bob: ", n_Bob)
print("|---------------------------|")

# Calculamos el Indicador de Euler phi:
phi_Alice = (primo_alice - 1) * (q_alice - 1)
print("Phi de Alice: ", phi_Alice)
print("|---------------------------|")

phi_Bob = (primo_bob - 1) * (q_bob - 1)
print("Phi de Bob: ", phi_Bob)
print("|---------------------------|")

# Por razones de eficiencia, tomaremos el número 4 de Fermat, que vale 65537, para el Indicador de Euler
# ya que es un número primo largo, que no es potencia de 2:
e = 65537

# Calcular la llave privada de Alice:
d_Alice = Crypto.Util.number.inverse(e, phi_Alice)
print("Llave privada de Alice: ", d_Alice)
print("|---------------------------|")

# Calcular la llave privada de Bob:
d_Bob = Crypto.Util.number.inverse(e, phi_Bob)
print("Llave privada de Bob: ", d_Bob)
print("|---------------------------|")

# Ahora Alice cifrará cada fragmento del mensaje previamente dividido en fragmentos de 128 caracteres


fragmentos_cifrados_por_Alice = []
for fragmento in mensaje_dividido_128_caracteres:
    mensaje_en_numero = int.from_bytes(bytes(fragmento.encode("utf-8")), "big")
    mensaje_cifrado = pow(mensaje_en_numero, e, n_Bob)
    fragmentos_cifrados_por_Alice.append(mensaje_cifrado)

print("Fragmentos cifrados: ", fragmentos_cifrados_por_Alice)
print("||||||––––––-|||||||")

# Ahora de su lado, Bob descifra los mensajes con su llave privada y con con cada uno de ellos
# obtendrá el mensaje original de 1050 caracteres

mensaje_descifrado = []
for fragmento_cifrado in fragmentos_cifrados_por_Alice:

    # Bob descifra utilizando su llave privada
    fragmento_descifrado = pow((fragmento_cifrado), d_Bob, n_Bob)

    # Convertir el número descifrado a una cadena de caracteres
    fragmento_descifrado_texto = long_to_bytes(fragmento_descifrado).decode("utf-8")

    #  Agregar el fragmento descifrado a la lista
    mensaje_descifrado.append(fragmento_descifrado_texto)

print("Mensaje descifrado por Bob: ", mensaje_descifrado)
print("|---------------------------|")

# Bob genera el hash del mensaje recibido
mensaje_descifrado_completo = ''.join(mensaje_descifrado)

hash_mensaje_recibido = SHA256.new(mensaje_descifrado_completo.encode("utf-8"))

# Comparamos el hash del mensaje recibido por Bob con el hash del mensaje original de Alice

print("Hash del mensaje original: ", "\n", hash_1050_caracteres.digest())
print("")
print("Hash del mensaje descifrado: ", "\n", hash_mensaje_recibido.digest())
print("")
if hash_mensaje_recibido.digest() == hash_1050_caracteres.digest():
    print("Los hashes coinciden.")
else:
    print("Los hashes no coinciden.")