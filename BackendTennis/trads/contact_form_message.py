from django.utils.translation import gettext_lazy as _

CONTACT_FORM_MESSAGE = {
    'SUCCESS': _('Mail send successfully.'),
    'ERROR': {
        'ERROR_OCCURRED': _('An error has occurred, please try again. If the error persists, '
                            'please contact your administrator.'),
        'FIRSTNAME_MAX_LENGTH': _('The Firstname must not exceed 40 characters.'),
        'LASTNAME_MAX_LENGTH': _('The Lastname must not exceed 40 characters.'),
        'PHONE_WRONG_FORMAT': _(
            'Enter a valid phone number.'
        ),
        'EMAIL_WRONG_FORMAT': _(
            'The Email address must be in a valid format (ex: <ADDRESS>@<DOMAIN>.com).'
        ),
        'SUBJECT_MAX_LENGTH': _('The Subject must not exceed 180 characters.'),
        'MESSAGE_MAX_LENGTH': _('The Message must not exceed 1000 characters.'),
    }
}
