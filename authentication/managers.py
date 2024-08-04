from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):

    # All user
    def create_user(self, email, password=None, **extra_fields):

        # if username is None:
        #     raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        if password is None:
            raise TypeError('Users must have a password.')

        username = extra_fields.pop('username', None)
        user = self.model(
            # 중복 최소화를 위한 정규화
            email=self.normalize_email(email),
            **extra_fields    # **extra_fields는 'username', 'email', 'password'를 제외한 필드
        )

        # django 에서 제공하는 password 설정 함수
        user.expiration_date = timezone.now() + timezone.timedelta(days=10)
        user.membership_level = 'N1'
        user.set_password(password)
        user.save()

        return user

    # admin user
    def create_superuser(self, email, password, **extra_fields):

        if password is None:
            raise TypeError('Superuser must have a password.')

        # "create_user"함수를 이용해 우선 사용자를 DB에 저장
        user = self.create_user(email, password, **extra_fields)
        # 관리자로 지정
        user.is_superuser = True
        user.is_staff = True
        user.is_terms_agreement = True
        user.is_info_use_agreement = True
        user.save()

        return user