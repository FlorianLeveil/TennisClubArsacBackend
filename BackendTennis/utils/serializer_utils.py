class SerializerUtils:
    @staticmethod
    def get_error_message(serializer):
        errors_message = []
        for key_error, errors in serializer.errors.items():
            for error in errors:
                errors_message.append(f'Error on key "{key_error}", code [{error.code}] : {str(error)}')
        return '\n'.join(errors_message)
