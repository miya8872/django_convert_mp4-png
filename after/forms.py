from django import forms
from .models import Items

class ItemsForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = ["video", "pin"]
        widgets = {
            "pin": forms.NumberInput(attrs={
                "min": 1000,
                "max": 9999,
                "required": "required",
                "placeholder": "数字4桁",
                "oninvalid": "this.setCustomValidity('4桁の数字を入力してください')",
                "oninput": "this.setCustomValidity('')",
                "style": "width: 120px;",
            })
        }
