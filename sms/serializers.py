from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'phone_number']



class SendSMSRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    message = serializers.CharField(required=True)

class SendBulkSMSRequestSerializer(serializers.Serializer):
    message = serializers.CharField(required=True)