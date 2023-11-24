import random
import string
import os
import keyboard

characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_-+=~`[]{}|;:'\",.<>/?\\"

def generate_random_string():
    length = random.randint(1, 7)
    return ''.join(random.choice(characters) for _ in range(length))

correct = 0

while True:
    os.system('cls')
    print(f"current score: {correct}")
    random_string = generate_random_string()
    print("=> " + random_string)
    x = input("=> ")
    if x == random_string:
        correct += 1
    else:
        correct -= 1
