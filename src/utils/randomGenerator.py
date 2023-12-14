import random

def get_random_string(length):
    left_limit = 97  # letter 'a'
    right_limit = 122  # letter 'z'

    random_chars = [chr(random.randint(left_limit, right_limit)) for _ in range(length)]
    random_string = ''.join(random_chars)

    return random_string