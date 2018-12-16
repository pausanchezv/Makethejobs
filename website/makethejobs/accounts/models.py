from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    """ User extending from AbstractUser"""

    email = models.EmailField('Email address', unique=True)
    about = models.TextField('About', blank=True, default='')
    headline = models.CharField('Headline', max_length=100, blank=True, default='')
    company = models.CharField('Company', max_length=100, blank=True, default='')
    area = models.CharField('Area', max_length=50, blank=True, default='')
    password_token = models.CharField('Forgotten Password Token', max_length=32, blank=True, default='')

    def __str__(self):
        """
        String override
        :return: string
        """
        return '{} <{}>'.format(self.username, self.email)
