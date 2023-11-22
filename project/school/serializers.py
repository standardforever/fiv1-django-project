from rest_framework import serializers
from .models import User, History
from rest_framework import status
from django.db import IntegrityError
from rest_framework.response import Response
from django.core.validators import MinLengthValidator, MaxLengthValidator



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name',
                  'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        extra_kwargs = {
            'username': {'required': True},
            'password': {'required': True},
            'first_name': {'required': True},

        }


    def create(self, validated_data):
        try:
            user = User(
                username=validated_data['username'],
                first_name=validated_data['first_name']
            )
            user.set_password(validated_data['password'])
            user.save()
            return user
        except IntegrityError as e:
            return Response({'error': 'Username (email) is already in use.'}, status=status.HTTP_400_BAD_REQUEST)


class HistorySerializer(serializers.ModelSerializer):
    word = serializers.CharField(
        required=True,
        validators=[
            MinLengthValidator(limit_value=1, message='Word must be at least 1 characters long.'),
            MaxLengthValidator(limit_value=4, message='Word cannot be longer than 4 characters.')
        ]
    )

    class Meta:
        model = History
        fields = ['user', 'word', 'is_error', 'date',  'error']
        extra_kwargs = {
            'word': {'required': True}
        }
    
    def create(self, validated_data):
        history = History(
            **validated_data
        )
        history.save()
        return history