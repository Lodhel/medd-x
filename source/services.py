import hashlib
import random
import string
import uuid


class General:

    def generate_token(self):
        result = str(uuid.uuid4())
        return result[0:32]

    def crypt(self, main_string):
        return hashlib.sha256(main_string.encode()).hexdigest()

    def generate_code(self, size=4, chars=string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
