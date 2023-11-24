import random
import string
import os
import keyboard

characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_-+=~`[]{}|;:'\",.<>/?\\"

def generate_random_string():
    length = random.randint(5, 11)
    output = ''.join(random.choice(characters) for _ in range(length))
    
    num_spaces = random.randint(1, 3)
    positions = random.sample(range(1, length - 1), num_spaces) 

    for pos in sorted(positions, reverse=True):
        output = output[:pos] + ' ' + output[pos:]
    
    return output

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
