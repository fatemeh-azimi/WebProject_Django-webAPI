from django.core.mail import EmailMessage
import threading
from templated_mail.mail import BaseEmailMessage


class EmailThread(threading.Thread):
    # overriding constructor
    def __init__(self, email_obj):
        # calling parent class constructor
        threading.Thread.__init__(self)
        self.email_obj = email_obj

    def run(self):
        self.email_obj.send()
