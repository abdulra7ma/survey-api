from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from .models import User


class RegisterationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        trim_whitespace=False,
        min_length=8,
    )
    password_confirmation = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "password",
            "password_confirmation",
        ]
        extra_kwargs = {
            "password": {
                "error_messages": {
                    "min_length": "Password can not be less than 8 characters."
                }
            },
        }

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "This email can not be use please use another one."
            )
        return email

    def validate(self, attrs):
        """check `password_confirmation` field if not equal `password` field"""

        if attrs["password_confirmation"] != attrs["password"]:
            raise serializers.ValidationError(
                "Password confirmation does not match the initail password"
            )
        return attrs

    def create(self, validated_data):
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        # creates a new user instance and ensures that password_confirmation
        # won't be passed to the create_user function
        instance = User.objects.create_user(
            email,
            password,
            **{
                k: v
                for k, v in validated_data.items()
                if not k == "password_confirmation"
            }
        )

        # activate the new registered account
        instance.is_active = True
        instance.save()

        return instance


class LogInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        label="Password",
        trim_whitespace=False,
        write_only=True,
        required=True,
        validators=[validate_password],
    )

    def validate(self, data):
        """
        checks user exists and password is correct.
        """

        try:
            User.objects.get(email=data["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid login or password.")

        authenticated_user = authenticate(
            username=data["email"],
            password=data["password"],
        )

        if not authenticated_user:
            raise AuthenticationFailed("Invalid login or password.")

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_administrator",
        ]


class RegisterionAdministratorSerializer(RegisterationSerializer):
    """
    Inherites the meta options of RegisterationSerializer and 
    comman attributes and overwrites the create function
    """

    class Meta(RegisterationSerializer.Meta):
        """
        Inherites the meta options of RegisterationSerializer
        """
    
    def create(self, validated_data):
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        # creates a new user instance and ensures that password_confirmation
        # won't be passed to the create_user function
        instance = User.objects.create_superuser(
            email,
            password,
            **{
                k: v
                for k, v in validated_data.items()
                if not k == "password_confirmation"
            }
        )

        # activate the new registered administrator account
        instance.save()

        return instance
