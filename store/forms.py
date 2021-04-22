from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Your last name.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Your first name.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    # phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$')
    # country = CountryField()
    city = forms.CharField(max_length=256)

    class Meta:
        model = User

        fields = ['username', 'first_name',
                  'last_name', 'email',
                  'password1',
                  "city"]
