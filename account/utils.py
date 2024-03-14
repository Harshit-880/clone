from django.core.mail import EmailMessage
from django.utils.encoding import force_str
from rest_framework import status
from rest_framework.exceptions import APIException
import os

class CustomValidation(APIException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, field, status_code):
        
        if status_code is None:
            self.status_code = self.default_status_code
        else:
            self.status_code = status_code
            
        if detail is None:
            self.detail = {'detail': force_str(self.default_detail)}
        else: 
            if(field == 'multiple'):
                self.detail = {"non_field_errors": force_str(detail)}
            else:
                self.detail = {field: force_str(detail)}

class Util:
  @staticmethod
  def send_email(data):
    email = EmailMessage(
      subject=data['subject'],
      body=data['body'],
      from_email=os.environ.get('EMAIL_FROM'),
      to=[data['to_email']]
    )
    email.send()