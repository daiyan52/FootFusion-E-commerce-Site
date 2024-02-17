from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.contrib.auth import get_user_model

class UserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(_('username'), max_length=264, null=True, blank=True)
    full_name = models.CharField(_('full name'), max_length=264,null=True, blank=True)
    address = models.CharField(_('address'), max_length=300, null=True, blank=True)
    city = models.CharField(_('city'), max_length=30, null=True, blank=True)
    state = models.CharField(_('state'), max_length=30, null=True, blank=True)
    zipcode = models.CharField(_('zipcode'), max_length=10, null=True, blank=True)
    country = models.CharField(_('country'), max_length=30, null=True, blank=True)
    phone = models.CharField(_('phone'), max_length=30, null=True, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    def __str__(self):
        return f"{self.username}'s profile"

    def is_fully_filled(self):
        fields_name = [f.name for f in self._meta.get_fields()]

        for field_name in fields_name:
            value = getattr(self, field_name)
            if value is None or value == '':
                return False
        return True

    def save_profile(self, **kwargs):
        self.save(**kwargs)

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
