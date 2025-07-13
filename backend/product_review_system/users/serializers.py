from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile

class RegisterSerializers(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'role']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User.objects.create_user(**validated_data)
        user.userprofile.role = role
        user.userprofile.save()
        return user