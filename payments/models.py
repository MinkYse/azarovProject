# payments/models.py
from django.db import models


class Trainer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def calculate_salary(self):
        total_children = sum(hall.get_child_count() for hall in self.hall_set.all())
        if total_children >= 10:
            return 10000 + 700 * total_children
        elif total_children >= 20:
            return 15000 + 700 * total_children
        elif total_children >= 40:
            return 20000 + 700 * total_children
        return sum(hall.get_income() for hall in self.hall_set.all()) - sum(hall.month_price + hall.additional_expenses for hall in self.hall_set.all())
        # return 10000 + 700 * total_children

    def is_salary_covered(self):
        # Рассчитываем, хватает ли средств на аренду и зарплату
        total_income = sum(hall.get_income() for hall in self.hall_set.all())
        total_rent = sum(hall.month_price + hall.additional_expenses for hall in self.hall_set.all())
        salary = self.calculate_salary()
        return total_income >= total_rent + salary

    class Meta:
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренеры'


class Hall(models.Model):
    name = models.CharField(max_length=100)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    month_price = models.DecimalField(max_digits=10, decimal_places=2)
    additional_expenses = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    def get_income(self):
        return sum(child.training_option.price for child in self.child_set.filter(is_paid=True, active=True))

    def is_enough_for_rent(self):
        return self.get_income() >= self.month_price + self.additional_expenses

    def get_child_count(self):
        return self.child_set.filter(is_paid=True).count()

    class Meta:
        verbose_name = 'Зал'
        verbose_name_plural = 'Залы'


class TrainingOption(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Parent(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Родитель'
        verbose_name_plural = 'Родители'


class SourceOfInfo(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Источник'
        verbose_name_plural = 'Источники'


class Child(models.Model):
    full_name = models.CharField(max_length=255)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    training_option = models.ForeignKey(TrainingOption, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    parents = models.ManyToManyField(Parent, blank=True)
    is_vip = models.BooleanField(default=False)
    source_of_info = models.ForeignKey(SourceOfInfo, on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'


class PDFDocument(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='pdfs/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'


class Application(models.Model):
    # email_subject = models.CharField(max_length=255)
    # email_sender = models.EmailField()
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=False)
    hall = models.ForeignKey(Hall, on_delete=models.SET_NULL, null=True, blank=True)
    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'