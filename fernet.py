from cryptography.fernet import Fernet

clave = Fernet.generate_key()

print("")
print("//////////----------------------//////////")
print("Esta es la clave del mensaje:", clave)
print("//////////----------------------//////////")
print("")

f = Fernet(clave)
# print(f)

# Cifra un texto
print("")
print("//////////----------------------//////////")
print("Este es el mensaje encriptado:")

texto_original = "El siguiente texto es un token, el que lo pueda descifrar tendrá el privilegio de deberme un electrolyt de la tienda de su preferencia"
token_encrypt = f.encrypt(texto_original.encode('utf-8'))
print(token_encrypt)
print("//////////----------------------//////////")
print("")

# Descifra el texto
texto_a_decifrar = "gAAAAABluwPSDHJ3Pi2kcuWbUs4UTYHJJ65NJ6Aw9f6JTD7r2TGLzZLFKNvJX2CVgIluQb6QbJy-Pnp_4zmIQFiFQJTydukRdoVPm215bDqPTeRZgg19awLqkGcJHMdv2uXgglVuJ2Lr"

# Esta linea es para decodificar la clave
clave_para_decifrar = "KazX6oDQZen_bhZNVvRVcGVJKqlzTjJ_ksiNm--WlPk="

# Esta linea es para cifrar el texto
f_para_decifrar = Fernet(clave_para_decifrar)

# Este es el texto descifrado
decrypt = (f_para_decifrar.decrypt(texto_a_decifrar))

print("")
print("//////////----------------------//////////")
print("El mensaje desencriptado es: ", decrypt)
print("//////////----------------------//////////")
print("")