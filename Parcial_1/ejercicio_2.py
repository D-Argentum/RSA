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
contrato_firmado_digitalmente_por_Alice = pow(hash_contrato_sin_firma_digital, d_Alice, n_Alice) # Revisar si está bien ??
print("Contrato firmado digitalmente por Alice:", contrato_firmado_digitalmente_por_Alice)
print("|----------------|")


# 2.- Alice agregará la firma digital al contrato

# Se creará un pdf de una página vacío y se agregará la firma digital:
def crear_pdf_firma_Alice(nombre_pdf):
    c = canvas.Canvas(nombre_pdf, pagesize=letter)

    contrato_firmado_digitalmente_por_Alice_str = str(contrato_firmado_digitalmente_por_Alice)

    # Calcular la longitud total y la longitud de cada línea
    longitud_total = len(contrato_firmado_digitalmente_por_Alice_str)
    longitud_linea = longitud_total // 10

    # Dividir el número entero en 10 líneas aproximadamente iguales
    lineas = [contrato_firmado_digitalmente_por_Alice_str[i:i + longitud_linea] for i in
              range(0, longitud_total, longitud_linea)]

    y = 100
    for linea in lineas:
        c.drawString(100, y, linea)
        y -= 10  # Disminuir la posición 'y' para la próxima línea

    c.save()

# Función para agregar la página de firma de Alice al PDF existente NDA.pdf
def agregar_firma_Alice_a_NDA(input_pdf, firma_pdf, output_pdf):
    # Abrir el PDF de entrada (NDA.pdf) y el PDF de la firma de Alice
    with open(input_pdf, "rb") as input_file, open(firma_pdf, "rb") as firma_file:
        reader_input = PyPDF2.PdfReader(input_file)
        reader_firma = PyPDF2.PdfReader(firma_file)

        writer = PyPDF2.PdfWriter()

        # Agregar páginas del PDF original (NDA.pdf) al nuevo PDF
        for page in reader_input.pages:
            writer.add_page(page)

        # Agregar la página de firma de Alice al final del nuevo PDF
        writer.add_page(reader_firma.pages[0])

        # Guardar el nuevo PDF
        with open(output_pdf, "wb") as output_file:
            writer.write(output_file)


# Nombre de los archivos PDF
nombre_NDA_pdf = "NDA.pdf"
nombre_firma_Alice_pdf = "firma_Alice.pdf"
nombre_NDA_firmado_pdf = "NDA_firmado_por_Alice.pdf"

# Crear el PDF de la firma de Alice
crear_pdf_firma_Alice(nombre_firma_Alice_pdf)

# Agregar la página de firma de Alice al PDF NDA.pdf y guardar el nuevo PDF firmado
agregar_firma_Alice_a_NDA(nombre_NDA_pdf, nombre_firma_Alice_pdf, nombre_NDA_firmado_pdf)

print("Se ha generado el PDF firmado por Alice.")
print("------------------|")


# Ahora Alice le envía el documento firmado a la Autoridad Certificadora

# 3.- La Autoridad Certificadora obtendrá el HASH del documento original.
# Ahora la autoridad verificará la autenticidad de la firma de Alice
documento_recibido_de_parte_de_Alice = contrato_firmado_digitalmente_por_Alice

# Ahora verificamos la firma de alice
verificacion_por_parte_de_la_autoridad = pow(documento_recibido_de_parte_de_Alice, e, n_Alice)
print("Hash que la autoridad verificará: ", verificacion_por_parte_de_la_autoridad)
print("|----------------|")

# Verificar si los hash coinciden
print("Verificación por parte de la Autoridad del hash: ", "\n", hash_contrato_sin_firma_digital)
print("------------------|")
print("Verificación de la firma de Alice: ", "\n", verificacion_por_parte_de_la_autoridad)
print("------------------|")

# Verificar si los hash coinciden
if verificacion_por_parte_de_la_autoridad == hash_contrato_sin_firma_digital:

    print("Los Hash del documento verificado y el Hash del documento original coinciden.")
else:
    print("Los Hash del documento verificado y el Hash del documento original no coinciden.")


# 4 - La Autoridad Certificadora firmará el documento con su llave privada y la agrega al PDF
# Asimismo se la envía a bob



contrato_firmado_digitalmente_por_la_ac = pow(verificacion_por_parte_de_la_autoridad, d_autoridad, n_autoridad) # Revisar si está bien ??
print("Contrato firmado digitalmente por la Autoridad:", contrato_firmado_digitalmente_por_la_ac)
print("|----------------|")

def crear_pdf_firma_Autoridad(nombre_pdf):
    c = canvas.Canvas(nombre_pdf, pagesize=letter)

    contrato_firmado_digitalmente_por_la_ac_str = str(contrato_firmado_digitalmente_por_la_ac)

    # Calcular la longitud total y la longitud de cada línea
    longitud_total = len(contrato_firmado_digitalmente_por_la_ac_str)
    longitud_linea = longitud_total // 10

    # Dividir el número entero en 10 líneas aproximadamente iguales
    lineas = [contrato_firmado_digitalmente_por_la_ac_str[i:i + longitud_linea] for i in
              range(0, longitud_total, longitud_linea)]

    y = 100
    for linea in lineas:
        c.drawString(100, y, linea)
        y -= 10  # Disminuir la posición 'y' para la próxima línea

    c.save()

# Función para agregar la página de firma de la autoridad al PDF existente NDA.pdf
def agregar_firma_Autoridad_a_NDA(input_pdf, firma_pdf, output_pdf):
    # Abrir el PDF de entrada (NDA.pdf) y el PDF de la firma de la autoridad
    with open(input_pdf, "rb") as input_file, open(firma_pdf, "rb") as firma_file:
        reader_input = PyPDF2.PdfReader(input_file)
        reader_firma = PyPDF2.PdfReader(firma_file)

        writer = PyPDF2.PdfWriter()

        # Agregar páginas del PDF original (NDA.pdf) al nuevo PDF
        for page in reader_input.pages:
            writer.add_page(page)

        # Agregar la página de firma de la autoridad al final del nuevo PDF
        writer.add_page(reader_firma.pages[0])

        # Guardar el nuevo PDF
        with open(output_pdf, "wb") as output_file:
            writer.write(output_file)


# Nombre de los archivos PDF
nombre_NDA_pdf = "NDA.pdf"
nombre_firma_Autoridad_pdf = "firma_Autoridad.pdf"
nombre_NDA_firmado_por_la_autoridad_pdf = "NDA_firmado_por_la_autoridad.pdf"

# Crear el PDF de la firma de la Autoridad
crear_pdf_firma_Autoridad(nombre_firma_Autoridad_pdf)

# Agregar la página de firma de Alice al PDF NDA.pdf y guardar el nuevo PDF firmado
agregar_firma_Alice_a_NDA(nombre_NDA_pdf, nombre_firma_Autoridad_pdf, nombre_NDA_firmado_por_la_autoridad_pdf)

print("Se ha generado el PDF firmado por la Autoridad.")
print("------------------|")


# Bob obtiene el HASH del documento PDF y verifica la firma de la AC con la llave pública de AC.

documento_recibido_de_parte_de_la_Autoridad_Certificadora = contrato_firmado_digitalmente_por_la_ac

# Ahora verificamos la firma de la autoridad
verificacion_por_parte_de_bob = pow(documento_recibido_de_parte_de_la_Autoridad_Certificadora, e, n_autoridad)
print("Hash que la autoridad verificará: ", verificacion_por_parte_de_bob)
print("|----------------|")

# Verificar si los hash coinciden
print("Verificación por parte de Bob del hash: ", "\n", hash_contrato_sin_firma_digital)
print("------------------|")
print("Verificación de la firma de la Autoridad: ", "\n", verificacion_por_parte_de_bob)
print("------------------|")

# Verificar si los hash coinciden
if verificacion_por_parte_de_la_autoridad == hash_contrato_sin_firma_digital:

    print("Los Hash del documento verificado y el Hash del documento original coinciden.")
else:
    print("Los Hash del documento verificado y el Hash del documento original no coinciden.")
