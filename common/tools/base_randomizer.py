import random
import string


def generate_random_string(length):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


def generate_email(first_part: str):
    domain = "@mail.ru"
    return f"{first_part}{domain}"
