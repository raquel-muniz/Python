import random

senha = random.sample(range(0, 9), 4)

while True: 
    palpite = input("Entre com queatro dígitos: ")

    for i, num in enumerate(palpite):
        if int(num) == senha[i]:
            print(f"{num}", end="")
        elif int(num) in senha:
            print("?", end="")
        else:
            print("x", end="")
    print()

    if [int (i) for i in palpite] == senha:
        print("Acertou", palpite)
        break

1234