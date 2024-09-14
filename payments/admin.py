# payments/admin.py
from django.contrib import admin
from .models import Trainer, Hall, TrainingOption, Parent, SourceOfInfo, Child, PDFDocument, Application


# Настройка отображения для модели Trainer
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('name', 'calculate_salary', 'is_salary_covered')

    def calculate_salary(self, obj):
        return obj.calculate_salary()  # Вызываем метод calculate_salary

    def is_salary_covered(self, obj):
        return obj.is_salary_covered()

    calculate_salary.short_description = 'Зарплата'
    is_salary_covered.short_description = 'Хватает средств'
    search_fields = ('name',)
    ordering = ('name',)


# Настройка отображения для модели Hall
class HallAdmin(admin.ModelAdmin):
    list_display = ('name', 'trainer', 'month_price',
                    'additional_expenses', 'is_enough_for_rent', 'get_child_count', 'get_income')

    def get_child_count(self, obj):
        return obj.get_child_count()

    def get_income(self, obj):
        return obj.get_income()

    get_child_count.short_description = 'Количество детей'
    get_income.short_description = 'Общая прибыль'

    list_filter = ('trainer',)
    search_fields = ('name', 'trainer__name')


# Настройка отображения для модели TrainingOption
class TrainingOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)


# Настройка отображения для модели Parent
class ParentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number')
    search_fields = ('full_name', 'phone_number')


# Настройка отображения для модели SourceOfInfo
class SourceOfInfoAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# Настройка отображения для модели Child
class ChildAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'hall', 'training_option', 'is_paid', 'is_vip')
    list_filter = ('is_paid', 'is_vip', 'hall', 'training_option')
    search_fields = ('full_name', 'hall__name', 'training_option__name')


# Настройка отображения для модели PDFDocument
class PDFDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'file')
    search_fields = ('title',)


# Настройка отображения для модели Application
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'status', 'hall', 'received_at')
    list_filter = ('status', 'hall', 'received_at')
    search_fields = ('name', 'phone')
    ordering = ('-received_at',)


# Регистрация всех моделей с кастомными настройками
admin.site.register(Trainer, TrainerAdmin)
admin.site.register(Hall, HallAdmin)
admin.site.register(TrainingOption, TrainingOptionAdmin)
admin.site.register(Parent, ParentAdmin)
admin.site.register(SourceOfInfo, SourceOfInfoAdmin)
admin.site.register(Child, ChildAdmin)
admin.site.register(PDFDocument, PDFDocumentAdmin)
admin.site.register(Application, ApplicationAdmin)
