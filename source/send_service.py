
from __future__ import print_function

import os
import re

import clicksend_client
from clicksend_client import SmsMessage, VoiceMessage
from clicksend_client.rest import ApiException
from clicksend_client import EmailRecipient
from clicksend_client import EmailFrom
from clicksend_client import Attachment

# Configure HTTP basic authorization: BasicAuth
configuration = clicksend_client.Configuration()
configuration.username = 'm.komlevski@gmail.com'
configuration.password = '2C92A044-ECD5-1DF6-A49D-040212AA8FF7'


class Sendor:
    def send_sms(self, phone, code):
        api_instance = clicksend_client.SMSApi(clicksend_client.ApiClient(configuration))

        sms_message = SmsMessage(source="php",
                                 body="Your security code for MEDD is {}".format(code),
                                 to=phone,
                                 schedule=1436874701)

        sms_messages = clicksend_client.SmsMessageCollection(messages=[sms_message])

        try:
            # Send sms message(s)
            api_response = api_instance.sms_send_post(sms_messages)
            print(api_response)
        except ApiException as e:
            print("Exception when calling SMSApi->sms_send_post: %s\n" % e)

    def send_voice_message(self, phone, code):
        api_instance = clicksend_client.VoiceApi(clicksend_client.ApiClient(configuration))
        # VoiceMessageCollection | VoiceMessageCollection model
        voice_message = VoiceMessage(source="php",
                        body="Hello. Your security code for MEDD is {}".format(code),
                        to=phone,
                        lang="en-au",
                        voice="female",
                        schedule="1436874701",
                        custom_string="this is a test",
                        require_input=1,
                        machine_detection=1,country="russia")
        voice_messages = clicksend_client.VoiceMessageCollection(messages=[voice_message])

        try:
            # Send voice message(s)
            api_response = api_instance.voice_send_post(voice_messages)
            print(api_response)
        except ApiException as e:
            print("Exception when calling VoiceApi->voice_send_post: %s\n" % e)

    def send_to_email(self, email, code):
        api_instance = clicksend_client.TransactionalEmailApi(clicksend_client.ApiClient(configuration))
        email_receipient = EmailRecipient(email=email, name='username')
        email_from = EmailFrom(email_address_id='14867', name='MEDD')
        attachment = Attachment(content='ZmlsZSBjb250ZW50cw==',
                              type='text/html',
                              filename='text.txt',
                              disposition='attachment',
                              content_id='292')
        # Email | Email model

        base_dir_template_start: str = "{}/templates/email_verify.html".format(os.path.dirname(os.path.abspath(__file__)))
        base_dir_template_end: str = "{}/templates/email_verify2.html".format(os.path.dirname(os.path.abspath(__file__)))
        template_start = open(base_dir_template_start, "r", encoding='utf-8')
        template_end = open(base_dir_template_end, "r", encoding='utf-8')
        template_start: str = template_start.read()
        template_end: str = template_end.read()

        template = template_start + code + template_end


        email = clicksend_client.Email(to=[email_receipient],
                                      cc=[email_receipient],
                                      bcc=[email_receipient],
                                      _from=email_from,
                                      subject="Test subject",
                                      body=template,
                                      attachments=[attachment])

        try:
            # Send transactional email
            api_response = api_instance.email_send_post(email)
            print(api_response)
        except ApiException as e:
            print("Exception when calling TransactionalEmailApi->email_send_post: %s\n" % e)
