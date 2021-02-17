from django import forms

from .models import Goods


class GoodsForm(forms.ModelForm):
    """Форма отзыва"""
    class Meta:
        model = Goods
        fields = ("code", "image", "url", "measurement")
        widgets = {
            "code": forms.TextInput(attrs={"class": "editContent"}),
            "image": forms.ImageField(attrs={"class": "editContent"}),
            "url": forms.SlugField(attrs={"class": "editContent"}),
            "measurement": forms.ChoiceField(attrs={"class": "editContent"}),
        }