n = input("Digite a posição da segunda sequencia de fibonacci: ")

if n<=0:
    print("Posição inválida")
elif n == 1:
    print(f"Sequencia de Fibonacci até {n}:\n [1]")
else:
    fibo=[1, 1]
    while len(fibo)<n:
        fibo = fibo + [fibo[- 1] + fibo[-2]]
    
print(f"Sequencia de Fibonacci até (n)", fibo)

