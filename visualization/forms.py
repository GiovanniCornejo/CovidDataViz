from django import forms
from django.core.exceptions import ValidationError

class MonthForm(forms.Form):
    month = forms.CharField(label='Month (numeric format)', max_length=2)

    def clean_month(self) -> int:
        month = self.cleaned_data.get("month")
        if not month.isdigit(): # type: ignore
            raise ValidationError("ERROR: Invalid Input")
        month = int(month) # type: ignore
        if month < 1 or month > 12:
            raise ValidationError("ERROR: Out of Range")
        return month