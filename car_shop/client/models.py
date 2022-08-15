from core.models import Base
from django.db import models
from django.contrib.auth.models import User


class Client(Base):
    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        db_table = 'client'

    SEX_CHOICES = (
        ('M', 'Man'),
        ('W', 'Woman'),
        ('-', 'None'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(default='', max_length=120)
    surname = models.CharField(default='', max_length=120)
    age = models.IntegerField(default=18)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='-')
    number = models.CharField(default='', blank=True, max_length=10)
    email = models.CharField(default='', max_length=120)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
