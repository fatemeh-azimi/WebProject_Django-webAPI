from rest_framework import serializers
from django.core import exceptions
from django.contrib.auth.password_validation import validate_password
from ...models import User, Profile
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.conf import settings

### import jwt #for EmailVerificationSerializer and PasswordResetTokenVerificationSerializer and SetNewPasswordSerializer



class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length = 255, write_only = True)
    class Meta:
        model = User
        fields = ["email", "password", "password1"]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError({"detail": "passswords doesnt match"})
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data.pop("password1", None)
        return User.objects.create_user(**validated_data)


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"), write_only=True)
    password = serializers.CharField(label=_("Password"), style={"input_type": "password"}, 
                                     trim_whitespace=False, write_only=True,)
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        username = attrs.get("email")
        password = attrs.get("password")
        if username and password:
            user = authenticate(request=self.context.get("request"), username=username, password=password,)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
            if not user.is_verified:
                raise serializers.ValidationError({"details": "user is not verified"})
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if not self.user.is_verified:
             raise serializers.ValidationError({"details": "user is not verified"})
        validated_data["email"] = self.user.email
        validated_data["user_id"] = self.user.id
        return validated_data


class JWTObtainPairTokenSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=6, write_only=True)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)
        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed(detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')
        attrs["user"] = user
        return super().validate(attrs)


class ChangePasswordSerialier(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("new_password1"):
             raise serializers.ValidationError({"detail": "passswords doesnt match"})
        try:
            validate_password(attrs.get("new_password"))
        except exceptions.ValidationError as e:
             raise serializers.ValidationError({"new_password": list(e.messages)})
        return super().validate(attrs)


class ChangePasswordSerializer2(serializers.Serializer):
    model = get_user_model

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password1"]:
            raise serializers.ValidationError(
                {"details": "Passwords does not match"}
            )
        return super().validate(attrs)


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email", read_only=True)
    # my_posts = Post.objects.filter(author="user")
    # my_posts = serializers.CharField(source="user.email", read_only=True)#, write_only = True)
    class Meta:
        model = Profile
        fields = ("id", "email", "first_name", "last_name", "image", "discription")#, "my_posts")
        read_only_fields = ["email"]

    # url که به صفحه پست ها میرود --->
    # http://127.0.0.1:8000/blog/api/v1/post/?category=&author=2&status=
    # <--


class ActivationResendSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'detail': 'user does not exist'})
        if user_obj.is_verified:
            raise serializers.ValidationError(
                {'detail': 'user is already activated and verified'}
            )
        attrs['user'] = user_obj
        return super().validate(attrs)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=600)
    class Meta:
        model = User
        fields = ['token']

    def validate(self, attrs):
        token = attrs['token']
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
        except jwt.ExpiredSignatureError as identifier:
            return ValidationError({'detail': 'Activation Expired'})
        except jwt.exceptions.DecodeError as identifier:
            raise ValidationError({'detail': 'Invalid token'})

        attrs["user"] = user
        return super().validate(attrs)


class PasswordResetTokenVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=600)

    class Meta:
        model = User
        fields = ['token']

    def validate(self, attrs):
        token = attrs['token']
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
        except jwt.ExpiredSignatureError as identifier:
            return ValidationError({'detail': 'Token expired'})
        except jwt.exceptions.DecodeError as identifier:
            raise ValidationError({'detail': 'Token invalid'})
        attrs["user"] = user
        return super().validate(attrs)


class SetNewPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=600)
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    password1 = serializers.CharField(min_length=6, max_length=68, write_only=True)

    class Meta:
        fields = ['password', 'password1', 'token']

    def validate(self, attrs):
        if attrs["password"] != attrs["password1"]:
            raise serializers.ValidationError({"details": "Passwords does not match"})
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            user.set_password(password)
            user.save()
            return super().validate(attrs)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)

