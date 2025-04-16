import re

from django import forms


class CreateOrderForm(forms.Form):
    username = forms.CharField()
    phone_number = forms.CharField()
    requires_delivery = forms.ChoiceField(choices=[("0", False),("1", True),],)
    delivery_address = forms.CharField(required=False)
    payment_on_get = forms.ChoiceField(choices=[("0", False),("1", True),],)

    def clean_phone_number(self):
        data = self.cleaned_data["phone_number"]
        pattern = re.compile(r'^\+\d{6,14}$')
        if not pattern.match(data):
            raise forms.ValidationError("Номер телефона должен начинаться с + и содержать только цифры, минимум 6.")
        return data
