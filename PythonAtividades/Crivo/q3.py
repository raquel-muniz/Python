n = int(input("Digite um número: "))

primos = [True] * (n+1)

primos[0:2] = [False, False]

lista = list(range(2, n+1))

for i in range(2, int((n**0.5)) +1):
    if primos[i]:
        for j in range(i*2, n+1, i):
            primos[j]=False

print([i for i, primo in enumerate(primos) if primo])
 
