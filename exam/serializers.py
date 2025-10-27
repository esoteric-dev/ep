from rest_framework import serializers
from exam.models import (
    Exam, 
    TestPaper,
    Question_type_mcq, 
    Question_type_numerical, 
    Question_type_msq, 
)

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'
        extra_kwargs = {
            '__all__': {'read_only': True},
        }

class TestPaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestPaper
        fields = '__all__'
        extra_kwargs = {
            '__all__': {'read_only': True},
        }

class QuestionTypeMCQSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question_type_mcq
        fields = '__all__'
        extra_kwargs = {
            '__all__': {'read_only': True},
        }

class QuestionTypeNumericalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question_type_numerical
        fields = '__all__'
        extra_kwargs = {
            '__all__': {'read_only': True},
        }

class QuestionTypeMSQSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question_type_msq
        fields = '__all__'
        extra_kwargs = {
            '__all__': {'read_only': True},
        }
# Note: All fields are set to read-only as per the requirement.