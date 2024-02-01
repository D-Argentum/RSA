from crypto.Util import number

import random

# Ejercicio 1:
print("Ejercicio 1 - Número aleatorio de 256 bits",'\n',random.getrandbits(256),'\n')

# Ejercicio 2:
print("Ejercicio 2 - Obtenemos un número primo de 1024 bits")
i = 0

while(True):
    i = i+1
    j = random.getrandbits(1024)
    esPrimo = number.isPrime(j)
    if (esPrimo):
        print("En la iteración <", i, "> se encontró el número primo <", j, ">","\n")
        break


# Ejercicio 3:

def inversoMultiplicativo (x,y):
    print("Ejercicio 3 - Obtenemos el inverso multiplicativo de un número x:<", "\n", x, ">\n", "y el número y: <", "\n", y, ">\n", "es: <", "\n", number.inverse(x,y), ">\n")

a = random.getrandbits(1024)
b = random.getrandbits(1024)

inversoMultiplicativo(a,b)    


# Ejercicio 4:
# Potencia de un número 2^(e) mod p, donde "e" es un número de 256 bits y "p" es un número primo de 1024 bits:

a = 2
b = random.getrandbits(256)
c = i

def potencia(x,y,z):
    print("Ejercicio 4 - La potencia de x a la y mod z, es: ", "\n", pow(x,y,z))

potencia(a,b,c)
    




