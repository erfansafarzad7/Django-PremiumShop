from django.contrib.auth.models import BaseUserManager
from accounts.validators import phone_number_validation
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, phone_number, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_("ایمیل را وارد کنید.."))
        if not phone_number:
            raise ValueError("شماره تلفن خود را وارد کنید..")
        if not phone_number_validation(phone_number):
            raise ValueError("شماره تلفن خود را به صورت : 09123456789 وارد کنید")

        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        user = self.create_user(email, phone_number, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True
        user.save(using=self._db)
        return user

