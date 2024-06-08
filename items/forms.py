from django import forms
from django.core.validators import RegexValidator


# alphabet_validator = RegexValidator(
#     r'^[a-zA-Z]*$',
#     'Only alphabet characters are allowed.'
# )


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100)

