from firebase_admin import auth
from django.conf import settings

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    CharField,
    as_serializer_error,
    BooleanField,
    SlugRelatedField
)

from allauth.account.utils import setup_user_email
from allauth.account.adapter import get_adapter

from rest_framework.serializers import ModelSerializer
from dj_rest_auth.serializers import LoginSerializer, UserDetailsSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer

User = get_user_model()


class CustomLoginSerializer(LoginSerializer):
    username = None

    @staticmethod
    def validate_auth_user_group(user):
        pass
        # if not user.groups.filter(name='admin').exists():
        #     raise ValidationError(_('User is not an Admin user.'))

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')
        user = self.get_auth_user(username, email, password)

        if not user:
            msg = _('Unable to log in with provided credentials.')
            raise ValidationError(msg)

        # Did we get back an active user?
        self.validate_auth_user_status(user)
        # Is the user in the correct group?
        # (e.g. admin, teacher, student)
        self.validate_auth_user_group(user)

        # If required, is the email verified?
        if 'dj_rest_auth.registration' in settings.INSTALLED_APPS:
            self.validate_email_verification_status(user, email=email)

        attrs['user'] = user
        return attrs


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    is_terms_agreed = BooleanField(default=False)

    def get_cleaned_data(self):
        cleaned_data = super().get_cleaned_data()
        cleaned_data['is_terms_agreed'] = self.validated_data.get(
            'is_terms_agreed', False)
        return cleaned_data

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                _("A user with this email address already exists."))
        return email

    def save(self, request):
        adapter = get_adapter()
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.new_user(request)
        user = adapter.save_user(request, user, self, commit=False)
        user.is_terms_agreed = self.cleaned_data['is_terms_agreed']

        password = self.cleaned_data.get('password1')
        if password:
            try:
                adapter.clean_password(password, user=user)
            except DjangoValidationError as exc:
                raise ValidationError(as_serializer_error(exc))

        # result = auth.create_user(email=user.email, password=password)
        # user.firebase_uid = result.uid
        user.firebase_uid = user.id.hex

        user.is_staff = True
        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class CustomUserDetailsSerializer(UserDetailsSerializer):
    """
    Nested serializer for User model to return only required fields.
    """
    groups = SlugRelatedField(many=True, read_only=True, slug_field="name")

    class Meta:
        model = User
        fields = UserDetailsSerializer.Meta.fields + \
            ('groups', 'phone', 'firebase_uid', 'is_terms_agreed')


class UserSerializer(ModelSerializer):
    """
    Nested serializer for User model to return only required fields.
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone']
