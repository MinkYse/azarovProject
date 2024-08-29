# payments/models.py
from django.db import models


class Hall(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Зал'
        verbose_name_plural = 'Залы'


class TrainingOption(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.price} руб."


class Parent(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f'fullname'


class Child(models.Model):
    full_name = models.CharField(max_length=255)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    training_option = models.ForeignKey(TrainingOption, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    parents = models.ManyToManyField(Parent, blank=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'
