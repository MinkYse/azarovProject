from django import forms
from .models import Hall, TrainingOption, Child


class PaymentForm(forms.Form):
    hall = forms.ModelChoiceField(queryset=Hall.objects.all(), label="Зал:")
    training_option = forms.ModelChoiceField(queryset=TrainingOption.objects.all(), label="Вариант обучения:")
    child = forms.ModelChoiceField(queryset=Child.objects.none(), label="Ребенок:")
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label="Сумма оплаты:", disabled=True, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hall'].queryset = Hall.objects.all()

        # Проверяем, был ли выбран зал
        if 'hall' in self.data:
            try:
                hall_id = int(self.data.get('hall'))
                self.fields['child'].queryset = Child.objects.filter(hall_id=hall_id)
            except (ValueError, TypeError):
                self.fields['child'].queryset = Child.objects.none()
        elif self.initial.get('hall'):
            hall_id = self.initial.get('hall').id
            self.fields['child'].queryset = Child.objects.filter(hall_id=hall_id)

        # Проверяем, был ли выбран вариант обучения
        if 'training_option' in self.data:
            try:
                option_id = int(self.data.get('training_option'))
                option = TrainingOption.objects.get(id=option_id)
                self.fields['amount'].initial = option.price
            except (ValueError, TypeError):
                self.fields['amount'].initial = None


class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['full_name', 'hall', 'training_option']
