from django.contrib.auth.models import User
from rest_framework import serializers
from student.models import ( 
    StudentProfile,
    ExamAttempt
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user 

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = '__all__'
        extra_kwargs = {
            'email': {'read_only': True}
        }

class ExamAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamAttempt
        fields = '__all__'
        extra_kwargs = {
            '__all__': {'read_only': True},
        }