import string
from random import choice


def generate_password(length=12):
    """
    Generate a random password
    """
    chars = string.ascii_letters + string.digits + string.punctuation
    return "".join(choice(chars) for _ in range(length))
