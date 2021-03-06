from __future__ import unicode_literals

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from . import constants


class Party(models.Model):
    date = models.DateField(null=True)
    deadline = models.DateField()

    users = models.ManyToManyField('User', through='UserRole')
    created_dt = models.DateTimeField(auto_now_add=True)


class UserRole(models.Model):
    user = models.ForeignKey('User')
    party = models.ForeignKey(Party)

    role = models.PositiveSmallIntegerField(choices=constants.UserRoleType.get_choices())


class GiftIdea(models.Model):
    user = models.ForeignKey('User')
    idea = models.TextField()

    party = models.ForeignKey(Party, null=True, blank=True)

    created_by = models.ForeignKey('User', related_name='+')
    created_dt = models.DateTimeField(auto_now_add=True)


class GiftIdeaComment(models.Model):
    idea = models.ForeignKey(GiftIdea)
    comment = models.TextField()

    created_by = models.ForeignKey('User', related_name='+')
    created_dt = models.DateTimeField(auto_now_add=True)


class GiftIdeaUpvote(models.Model):
    idea = models.ForeignKey(GiftIdea)

    created_by = models.ForeignKey('User', related_name='+')
    created_dt = models.DateTimeField(auto_now_add=True)


class FundContribution(models.Model):
    user = models.ForeignKey('User')
    amount = models.IntegerField()

    created_dt = models.DateTimeField(auto_now_add=True)


class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            last_login=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, False, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    birthday = models.DateField()
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.')
    )
    name = models.CharField(_('name'), max_length=30, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['birthday']

    objects = UserManager()

    def get_short_name(self):
        return self.name

    def get_full_name(self):
        return self.name
