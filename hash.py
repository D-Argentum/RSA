import hashlib

# Hacer un HASH de una cadena de texto de 8 bits
cadena_8_bits = "a"
num_bits_cadena_8_bits = len(cadena_8_bits.encode()) * 8
print("Longitud de la cadena de texto de 8 bits:", num_bits_cadena_8_bits)
print("|----------------|")

hash_8_bits = hashlib.sha256(cadena_8_bits.encode()).hexdigest()
print("HASH de una cadena de texto de 8 bits:", hash_8_bits)
print("|----------------|")

# HASH de una cadena de texto de 1024 bits
cadena_1024_bits = "¡Bienvenido a nuestro mundo de posibilidades infinitas! Descubre, aprende y crece. Juntos alcanzaremos grandes logros, sisisis."
num_bits_cadena_1024_bits = len(cadena_1024_bits.encode()) * 8
print("Longitud de la cadena de texto de 1024 bits:", num_bits_cadena_1024_bits)
print("|----------------|")

hash_1024_bits = hashlib.sha256(cadena_1024_bits.encode()).hexdigest()
print("HASH de una cadena de texto de 1024 bits:", hash_1024_bits)
print("|----------------|")

# Hacer un HASH de un archivo PDF

def hash_archivo(nombre_archivo):
    with open(nombre_archivo, "rb") as archivo:
        contenido = archivo.read()
        hash_archivo = hashlib.sha256(contenido).hexdigest()
        return hash_archivo

nombre_archivo_pdf_1 = "archivo_pdf.pdf"
nombre_archivo_pdf_2 = "archivo2_pdf.pdf"
nombre_archivo_pdf_3 = "archivo3_pdf.pdf"

# Calcular el hash para el primer archivo
hash_pdf_1 = hash_archivo(nombre_archivo_pdf_1)
print("HASH del primer archivo PDF:", hash_pdf_1)
print("|----------------|")

# Calcular el hash para el segundo archivo
hash_pdf_2 = hash_archivo(nombre_archivo_pdf_2)
print("HASH del segundo archivo PDF:", hash_pdf_2)
print("|----------------|")

# Calcular el hash para el segundo archivo
hash_pdf_3 = hash_archivo(nombre_archivo_pdf_3)
print("HASH del tercer archivo PDF:", hash_pdf_3)
print("|----------------|")

# Comparar los hashes
if hash_pdf_1 == hash_pdf_2:
    print("Los hashes del primer archivo PDF y el del segundo archivo PDF son iguales.", "\n","Primer Hash: ", "\n", hash_pdf_1, "\n","Segundo Hash: ", "\n", hash_pdf_2,)
else:
    print("Los hashes del primer archivo PDF y el del segundo archivo PDF son diferentes.", "\n", "Primer Hash: ", "\n", hash_pdf_1, "\n", "Segundo Hash: " "\n", hash_pdf_2,)
print("|----------------|")

# Comparar los hashes
if hash_pdf_1 == hash_pdf_3:
    print("Los hashes del primer archivo PDF y el del tercer archivo PDF son iguales.", "\n", "Primer Hash: ", "\n",hash_pdf_1, "\n" , "Tercer Hash: ", "\n", hash_pdf_3,)
else:
    print("Los hashes del primer archivo PDF y el del tercer archivo PDF son diferentes.", "\n", "Primer Hash: ", "\n", hash_pdf_1, "\n", "Tercer Hash: ", "\n", hash_pdf_3,)