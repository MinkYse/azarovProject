# payments/models.py
from django.db import models


class Hall(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TrainingOption(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.price} руб."


class Child(models.Model):
    full_name = models.CharField(max_length=255)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    training_option = models.ForeignKey(TrainingOption, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
