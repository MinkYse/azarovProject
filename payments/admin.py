# payments/admin.py
from django.contrib import admin
from .models import Hall, TrainingOption, Child, Parent

admin.site.register(Hall)
admin.site.register(TrainingOption)
admin.site.register(Child)
admin.site.register(Parent)