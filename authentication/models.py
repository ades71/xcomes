import jwt
from datetime import datetime, timedelta
from django.conf import settings

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.fields import BooleanField

from .managers import UserManager
from core.models import TimestampedModel
from importlib import import_module


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    # username = models.CharField(verbose_name='email', max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    name = models.CharField(max_length=10)
    nickname = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=255)
    # created_at = models.DateTimeField(null=True)
    # updated_at = models.DateTimeField(null=True)
    expiration_date = models.DateTimeField(null=True)
    membership_level = models.CharField(max_length=10)
    is_terms_agreement = models.BooleanField(default=False)
    is_info_use_agreement = models.BooleanField(default=False)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    # session_key = models.CharField(max_length=40, editable=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = [
        'name',
        'nickname',
        'phone_number'
    ]

    objects = UserManager()
    # SessionsStore = import_module(settings.SESSION_ENGINE).SessionStore

    # def kicked_my_other_sessions(sender, request, user, **kwargs):
    #     for user_session in User.objects.filter(user=user):
    #         session_key = user_session.session_key
    #         session = SessionStore(session_key)
    #         session.delete()
    #
    #     session_key = request.session.session_key
    #     user.objects.create(user=user, session_key=session_key)
    #
    # user_logged_in.connect(kicked_my_other_sessions, dispatch_uid='user_logged_in')
    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    # @property
    # def access_token(self):
    #     return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)
        token = jwt.encode({
            'id': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')

        return token
