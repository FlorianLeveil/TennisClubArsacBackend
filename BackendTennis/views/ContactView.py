import logging

from django.conf import settings
from django.core.mail import send_mail
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from BackendTennis.serializers import ContactFormSerializer

logger = logging.getLogger('BackendTennis.view.CONTACT')


class ContactView(APIView):
    permission_classes = []

    @extend_schema(
        summary='Send a contact message',
        request=ContactFormSerializer,
        responses={status.HTTP_200_OK: {'description': 'Message sent successfully'}},
        tags=['Contact']
    )
    def post(self, request, *args, **kwargs):
        serializer = ContactFormSerializer(data=request.data)

        if serializer.is_valid():
            contact_data = serializer.validated_data
            try:
                send_mail(
                    subject=f'Message from {contact_data['firstname']} {contact_data['lastname']}'
                            f', Subject : {contact_data['subject']}',
                    message=f'Email: {contact_data['email']}\n\n'
                            f'Phone: {contact_data['phone_number']}\n\n'
                            f'Message:\n{contact_data['message']}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=settings.CONTACT_EMAIL_RECIPIENTS,
                    fail_silently=False,
                )
                return Response({'message': 'Message sent successfully'}, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f'Error while sending mail : {str(e)}')
                return Response({'error': f'Error while sending : {str(e)}'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
