from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserRegistrationForm(UserCreationForm):
    fio = forms.CharField(label="ФИО", max_length=255, required=True)
    phone = forms.CharField(label="Телефон", max_length=20, required=True)
    email = forms.EmailField(label="Email", required=True)
    consent = forms.BooleanField(label="Согласие на обработку персональных данных", required=True)

    class Meta:
        model = User
        fields = ("username", "email", "fio", "phone", "password1", "password2", "consent")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                fio=self.cleaned_data['fio'],
                phone=self.cleaned_data['phone'],
                consent=self.cleaned_data['consent'],
            )
        return user
