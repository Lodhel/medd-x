import hashlib
import random
import string
import uuid
from twilio.rest import Client


class Twillio:

    def send(self, phone, sms_code):
        account_sid = "AC587271b41b5c9262e16153e6d0cfbb5b"
        auth_token = "a1781f76fbcfd53b4e8a869a30a9de4e"
        client = Client(account_sid, auth_token)

        message = client.messages \
                        .create(
                            body="Medicine Service\r\n",
                            from_='+15017122661',
                            to='+12569800351'
                         )

        print(message.sid)


class General:

    def generate_token(self):
        result = str(uuid.uuid4())
        return result[0:32]

    def crypt(self, main_string):
        return hashlib.sha256(main_string.encode()).hexdigest()

    def generate_code(self, size=4, chars=string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
