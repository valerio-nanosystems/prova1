lista = [1, 2 , 3 , 4]
lista.append(5)

for p in lista:
    if p % 2 == 0:
        print(str(p) + " è pari")
    else:
        print(str(p) + " è dispari")