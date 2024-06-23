from django import forms
from .models import Medicine

class MedicineForm(forms.ModelForm):
    expiry_date = forms.DateField(input_formats=['%d/%m/%Y'])

    class Meta:
        model = Medicine
        fields = ['name', 'identification_number', 'expiry_date','quantity']