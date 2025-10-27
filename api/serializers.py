from django.contrib.auth.models import User
from rest_framework import serializers
from student.models import StudentProfile


class UserSerializer(serializers.ModelSerializer):
	# Accept phone_number from client though not a field on User
	phone_number = serializers.CharField(write_only=True, required=False, allow_blank=True)
	password = serializers.CharField(write_only=True, min_length=6)

	class Meta:
		model = User
		fields = [
			'id',
			'username',
			'email',
			'password',
			'phone_number',
		]
		extra_kwargs = {
			'email': {'required': True},
		}

	def validate_email(self, value):
		# Ensure email unique across User or StudentProfile
		if User.objects.filter(email__iexact=value).exists():
			raise serializers.ValidationError('A user with this email already exists.')
		if StudentProfile.objects.filter(email__iexact=value).exists():
			raise serializers.ValidationError('A student profile with this email already exists.')
		return value

	def create(self, validated_data):
		phone = validated_data.pop('phone_number', '').strip()
		password = validated_data.pop('password')
		user = User(
			username=validated_data.get('username'),
			email=validated_data.get('email')
		)
		user.set_password(password)
		user.save()

		# Create a related StudentProfile record
		StudentProfile.objects.create(
			user=user,
			first_name=user.first_name or '',
			last_name=user.last_name or '',
			email=user.email,
			phone_number=phone or None,
		)
		return user

