from django.utils.translation import gettext_lazy as _

IMAGES_MESSAGES = {
    'SUCCESS': _('All images uploaded successfully.'),
    'ERROR': {
        'ERROR_OCCURRED': _('An error has occurred, please try again. If the error persists, '
                            'please contact your administrator.'),
        'INVALID_FORMAT': _('Invalid format : {error_message}'),
        'NO_IMAGE_FOUND': _('No image data received.'),
        'NO_INDEX_ON_IMAGE': _('Image data should have an index to correspond to image File : [{image_title}]'),
        'FILE_NOT_FOUND': _('Image file not found for image with index : [{image_index}]'),
        'SAVE_ERROR': _('Error occurred on image save : {error}'),
        'INCOMPLETE_SAVE': _('Some images could not be uploaded.'),
    }

}
