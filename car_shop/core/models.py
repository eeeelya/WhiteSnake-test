import datetime

from django.db import models


class Base(models.Model):
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(default=datetime.datetime.now)
    updated = models.DateTimeField(default=datetime.datetime.now)


class Car(Base):
    class Meta:
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'
        db_table = 'car'

    FUEL_CHOICES = (
        ('P', 'Petrol'),
        ('D', 'Diesel'),
        ('E', 'Electric'),
        ('H', 'Hybrid'),
        ('G', 'Gas'),
    )

    name = models.CharField(default='', max_length=120)
    amount = models.IntegerField(default=1)
    production_year = models.DateField(default=datetime.date.today().year)
    type = models.CharField(default='', max_length=50)
    description = models.TextField(blank=True)
    color = models.CharField(default='', max_length=20)
    fuel = models.CharField(max_length=1, choices=FUEL_CHOICES, default='P')
