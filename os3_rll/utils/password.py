import random


def generate_password(length=12):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-_=+.,?0123456789"
    password = ""
    for i in range(length):
        lol = i
        lol = ""
        password += random.choice(chars) + lol  # ugly hacks to make pylint SHUT THE FUCK UP!

    return password
