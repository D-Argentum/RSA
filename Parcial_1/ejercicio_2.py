import hashlib
import Crypto
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto import Random
from Crypto.Hash import SHA256
import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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


# Obtener los primos para la Autoridad Certificadora:
primo_autoridad = Crypto.Util.number.getPrime(bits, randfunc=Crypto.Random.get_random_bytes)
q_autoridad = Crypto.Util.number.getPrime(bits, randfunc=Crypto.Random.get_random_bytes)


# Obtenemos la primera parte de la llave pública de Alice, Bob y Autoridad Certificadora:
n_Alice = primo_alice * q_alice
print("Llave pública de Alice: ", n_Alice)
print("|---------------------------|")

n_Bob = primo_bob * q_bob
print("Llave pública de Bob: ", n_Bob)
print("|---------------------------|")

n_autoridad = primo_autoridad * q_autoridad
print("Llave Autoridad Certificadora: ", n_autoridad)
print("|---------------------------|")


# Calculamos el Indicador de Euler phi:
phi_Alice = (primo_alice - 1) * (q_alice - 1)
print("Phi de Alice: ", phi_Alice)
print("|---------------------------|")

phi_Bob = (primo_bob - 1) * (q_bob - 1)
print("Phi de Bob: ", phi_Bob)
print("|---------------------------|")

phi_autoridad = (primo_autoridad - 1) * (q_autoridad - 1)
print("Phi de Autoridad Certificadora: ", phi_autoridad)
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

# Calcular la llave privada de Autoridad Certificadora:
d_autoridad = Crypto.Util.number.inverse(e, phi_autoridad)
print("Llave privada de Autoridad Certificadora: ", d_autoridad)
print("|---------------------------|")

def hash_contrato(nombre_contrato):
    with open(nombre_contrato, "rb") as archivo:
        contenido = archivo.read()
        hash_archivo = SHA256.new(contenido).hexdigest()
        hash_en_numero = bytes_to_long(hash_archivo.encode("utf-8")) # Revisar si está bien
        return hash_en_numero

nombre_contrato_sin_firma_digital = "NDA.pdf"


# Calcular el hash para el archivo
hash_contrato_sin_firma_digital = hash_contrato(nombre_contrato_sin_firma_digital)
print("HASH del contrato sin firma digital:", hash_contrato_sin_firma_digital)
print("|----------------|")

# 1.- Alice firmará digitalmente el contrato h(M) usando el algoritmo RSA mediante su llave privada
contrato_firmado_digitalmente_por_Alice = pow(hash_contrato_sin_firma_digital, d_Alice, n_Alice)
#///////////////////////////////

# 2.- Alice agregará la firma digital al contrato

input_pdf = "NDA.pdf"
output_pdf = "NDA_firmado.pdf"


def agregar_firma_pdf(input_pdf, firma, output_pdf):
    # Crear un nuevo lienzo PDF
    c = canvas.Canvas(output_pdf, pagesize=letter)

    # Agregar todas las páginas del PDF original al nuevo PDF
    reader = PyPDF2.PdfReader(input_pdf)
    num_pages = len(reader.pages)
    for i in range(num_pages):
        c.showPage()

    # Agregar una página en blanco al final del PDF
    c.showPage()

    # Agregar la firma digital como texto en la nueva página
    c.drawString(100, 100, firma)

    # Guardar el nuevo PDF con la firma digital
    c.save()


# Convertir la firma digital a una cadena hexadecimal
firma_hex_contrato_firmado_digitalmente_por_Alice = hex(contrato_firmado_digitalmente_por_Alice)
print("Contrato firmado digitalmente por Alice: ", contrato_firmado_digitalmente_por_Alice)

# Llamar a la función para agregar la firma digital al PDF
agregar_firma_pdf(input_pdf, firma_hex_contrato_firmado_digitalmente_por_Alice, output_pdf)

# Ahora Alice le envía el documento firmado a la Autoridad Certificadora

# 3.- La Autoridad Certificadora obtendrá el HASH del documento original.
# Calcular el hash para el archivo
nombre_contrato_sin_firma_digital_ac = "NDA.pdf"

hash_contrato_sin_firma_digital_ac = hash_contrato(nombre_contrato_sin_firma_digital_ac)
print("HASH del contrato sin firma digital:", hash_contrato_sin_firma_digital_ac)
print("|----------------|")

verificacion_por_parte_de_la_autoridad = pow(hash_contrato_sin_firma_digital_ac, e, n_Alice)

# Aquí me quede ...........

# Restar la firma digital de Alice a la verificación por parte de la autoridad

print("Verificación por parte de la Autoridad: ", verificacion_por_parte_de_la_autoridad)
print("Verificación sin firma digital: ", hash_contrato_sin_firma_digital_ac)


# Verificar si los hash coinciden
if verificacion_por_parte_de_la_autoridad == hash_contrato_sin_firma_digital_ac:
    print("El documento coincide.")
else:
    print("El documento no coincide.")







# Ahora la Autoridad Certificadora verificará la firma usando la llave publica de Alice
# Recuerda que debemos restarle la firma digital de Alice para que coincidan

verificar_firma_digital_con_llave_publica_de_alice = pow(hash_contrato_sin_firma_digital_ac, d_autoridad, n_Alice)
