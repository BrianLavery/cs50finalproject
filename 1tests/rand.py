import random

n = random.randint(1,2)

print(f"n = {n}")

x = [1, 2, 3, 4, 5, 6]
random.shuffle(x)
print(f"x = {x}")

y = random.randint(0,1)
print(f"y = {y}")

newList = list(range(0,10))
print(newList)

numCtrs = list(range(0,255))
z = random.sample(numCtrs, k=10, counts=None)
print(z)