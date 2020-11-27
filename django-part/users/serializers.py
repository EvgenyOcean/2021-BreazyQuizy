from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import CustomUser # new user model

class UserRegisterSerializer(serializers.ModelSerializer):
    '''
    Validates user model fields. 
    If everything is correct, saves the user and returns current user object
    '''
    # overriding email to make sure it's unique
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=CustomUser.objects.all())]
            )
    # overriding username to make sure its max_length 32
    # and it's also unique
    username = serializers.CharField(
            max_length=32,
            required=True,
            validators=[UniqueValidator(queryset=CustomUser.objects.all())]
            )
    # overriding password to make sure that's its mix_length is 8
    # and write_only, so we don't get as an output
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
             validated_data['password'])
        return user

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')