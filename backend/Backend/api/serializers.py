# # from rest_framework import serializers
# # from .models import driver, citizen


# # # Serializer for the driver model
# # class DriverSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = driver
# #         fields = ['citizenship_no', 'first_name','last_name', 'email', 'password', 'address']

# # # Serializer for the citizen model
# # class CitizenSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = citizen
# #         fields = ['citizenship_no', 'first_name','last_name', 'email', 'password', 'address']
        
        

from base64 import urlsafe_b64decode, urlsafe_b64encode
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import driver, citizen
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_bytes



User = get_user_model()

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = driver  # Replace 'driver' with your actual model name
        fields = ['citizenship_no', 'first_name', 'last_name', 'email', 'password', 'address']

class CitizenSerializer(serializers.ModelSerializer):
    class Meta:
        model = citizen  # Replace 'citizen' with your actual model name
        fields = ['citizenship_no', 'first_name', 'last_name', 'email', 'password', 'address']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        label=_("Confirm Password"),
    )

    class Meta:
        model = User
        fields = ['citizenship_no', 'first_name', 'last_name', 'email', 'password', 'password2', 'address']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password2')
        if password != password2:
            raise serializers.ValidationError(_("Passwords do not match."))
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']

class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError(_("Passwords do not match."))
        user = self.context.get('user')
        user.set_password(password)
        user.save()
        return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_b64encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://localhost:8000/api/user/reset/'+uid+'/'+token
            body = 'Click the following link to reset your password: '+link
            data = {
                'subject': 'Reset Your Password',
                'body': body,
                'to_email': user.email
            }
            return attrs
        else:
            raise serializers.ValidationError(_("You are not a registered user."))

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        uid = self.context.get('uid')
        token = self.context.get('token')
        if password != password2:
            raise serializers.ValidationError(_("Passwords do not match."))
        try:
            id = smart_str(urlsafe_b64decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError(_("Token is not valid or has expired."))
            user.set_password(password)
            user.save()
            return attrs
        except UnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not Valid or Expired')


