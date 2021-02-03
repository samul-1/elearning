from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from .models import GlobalProfile


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        widget=TextInput(
            attrs={
                "placeholder": "Username",
            }
        ),
    )
    email = forms.EmailField(widget=TextInput(attrs={"placeholder": "Email"}))
    password1 = forms.CharField(widget=PasswordInput(attrs={"placeholder": "Password"}))
    password2 = forms.CharField(
        widget=PasswordInput(attrs={"placeholder": "Conferma password"})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        help_texts = {
            "username": "",
            "password1": "La password deve contenere almeno 8 caratteri, non tutti numerici, e non deve essere una stringa comunemente utilizzata.",
            "password2": "Inserisci nuovamente la stessa password.",
            "email": "L'indirizzo email verrà utilizzato nel caso in cui dovessi resettare la tua password.",
        }

    def save(self, force_insert=False, force_update=False):
        new_user = super(RegisterForm, self).save(self)

        # create global profile for user
        global_profile = GlobalProfile(user=new_user)
        global_profile.save()

        return new_user


class LoginFormWithPlaceholders(AuthenticationForm):
    username = forms.CharField(
        widget=TextInput(
            attrs={
                "class": "validate",
                "placeholder": "Username",
            }
        )
    )
    password = forms.CharField(widget=PasswordInput(attrs={"placeholder": "Password"}))
