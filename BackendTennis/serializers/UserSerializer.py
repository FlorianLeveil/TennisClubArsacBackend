from django.core.validators import RegexValidator
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from BackendTennis.models import User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    birthdate = serializers.DateField()
    email = serializers.EmailField(unique=True)
    phone_number = PhoneNumberField()
    postal_code = serializers.CharField(max_length=10, validators=[RegexValidator(regex=r'^\d{5}$', message="Le code postal doit être composé de 5 chiffres.")])
    address = serializers.CharField(max_length=500)
    street = serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100)
    spouse = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True)
    children = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, allow_empty=True)
    createAt = serializers.DateTimeField(read_only=True)
    updateAt = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        children_data = validated_data.pop('children', [])
        spouse_data = validated_data.pop('spouse', None)

        user = User.objects.create(**validated_data)

        # Création des enfants
        children = []
        for child_data in children_data:
            child_data['parent'] = user
            child_data = self._set_child_data_or_spouse_data(child_data, user)
            child_serializer = self.__class__(data=child_data)
            child_serializer.is_valid(raise_exception=True)
            child = child_serializer.save()
            children.append(child)

        user.children.set(children)

        # Création du conjoint (spouse)
        if spouse_data:
            spouse_data['spouse'] = user
            spouse_data = self._set_child_data_or_spouse_data(spouse_data, user)
            spouse_serializer = self.__class__(data=spouse_data)
            spouse_serializer.is_valid(raise_exception=True)
            spouse = spouse_serializer.save()
            user.spouse = spouse
            user.save()

        return user
    
    
    @staticmethod
    def _set_child_data_or_spouse_data(user, data):
        data['last_name'] = data['last_name'] if data['last_name'] else user.last_name
        data['email'] = data['email'] if data['email'] else user.email
        data['phone_number'] = data['phone_number'] if data['phone_number'] else user.phone_number
        data['postal_code'] = data['postal_code'] if data['postal_code'] else user.postal_code
        data['address'] = data['address'] if data['address'] else user.address
        data['street'] = data['street'] if data['street'] else user.street
        data['city'] = data['city'] if data['city'] else user.city
        data['country'] = data['country'] if data['country'] else user.country
        return data
        
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'birthdate',
            'email',
            'phone_number',
            'postal_code',
            'address',
            'street',
            'city',
            'country',
            'spouse',
            'children',
            'createAt',
            'updateAt'
        )
        read_only_fields = ('createAt', 'updateAt')
