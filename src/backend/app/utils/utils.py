import random
import string


def generate_random_string(n: int, src_chars=string.ascii_letters + string.digits) -> str:
    return ''.join(random.choice(src_chars) for _ in range(n))
