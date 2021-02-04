import hashlib
import random
import string
import uuid
from twilio.rest import Client


class Twillio:

    def send_sms(self, phone, sms_code):
        """
                TEST ACCOUNT SID
        AC680515c14f185ac882b8006c81dce7a0

        TEST AUTHTOKEN
        f96557e8d790c80e76507628dd3de33c
        """
        account_sid = "AC680515c14f185ac882b8006c81dce7a0"
        auth_token = "f96557e8d790c80e76507628dd3de33c"
        client = Client(account_sid, auth_token)

        message = client.messages \
                        .create(
                            body="Medicine Service\r\n",
                            from_='+79796243671',
                            to='+12569800351'
                         )

        print(message.sid)

    def send_mail(self, email=None, text=None):
        # Download the helper library from https://www.twilio.com/docs/python/install
        """
            https://www.twilio.com/docs/verify/email
            MEDD_dev
            API Key ID: 6RFOZOTqQwyhomWRUUt8aA
            API Key: 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
        """

        # Your Account Sid and Auth Token from twilio.com/console
        # and set the environment variables. See http://twil.io/secure
        account_sid = "AC680515c14f185ac882b8006c81dce7a0"
        auth_token = "f96557e8d790c80e76507628dd3de33c"
        client = Client(account_sid, auth_token)

        verification = client.verify \
            .services('2qJnuyR0980hqmdzkLUnnjcf-DAv1mcRtHwfegFtedg') \
            .verifications \
            .create(to='recipient@foo.com', channel='email')

        print(verification.sid)


class General:

    def generate_token(self):
        result = str(uuid.uuid4())
        return result[0:32]

    def crypt(self, main_string):
        return hashlib.sha256(main_string.encode()).hexdigest()

    def generate_code(self, size=4, chars=string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
