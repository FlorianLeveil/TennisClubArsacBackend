from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from BackendTennis.trads.contact_form_message import CONTACT_FORM_MESSAGE


class ContactFormSerializer(serializers.Serializer):
    firstname = serializers.CharField(max_length=40, error_messages={
        'max_length': CONTACT_FORM_MESSAGE['ERROR']['FIRSTNAME_MAX_LENGTH']
    })
    lastname = serializers.CharField(max_length=40, error_messages={
        'max_length': CONTACT_FORM_MESSAGE['ERROR']['LASTNAME_MAX_LENGTH']
    })
    phone_number = PhoneNumberField(region='FR', error_messages={
        'invalid': CONTACT_FORM_MESSAGE['ERROR']['PHONE_WRONG_FORMAT']
    })
    email = serializers.EmailField(error_messages={
        'invalid': CONTACT_FORM_MESSAGE['ERROR']['EMAIL_WRONG_FORMAT']
    })
    subject = serializers.CharField(max_length=180, error_messages={
        'max_length': CONTACT_FORM_MESSAGE['ERROR']['SUBJECT_MAX_LENGTH']
    })
    message = serializers.CharField(max_length=1000, error_messages={
        'max_length': CONTACT_FORM_MESSAGE['ERROR']['MESSAGE_MAX_LENGTH']
    })
