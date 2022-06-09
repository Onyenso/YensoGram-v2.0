from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Post


class UserRegisterForm(UserCreationForm):

    class Meta:

        model = User

        fields = ["username", "email", "password1", "password2"]

        # widgets = {
        #     "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
        #     "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
        #     "password1": forms.TextInput(attrs={"class": "form-control", "placeholder": "Password1"}),
        #     "password2": forms.TextInput(attrs={"class": "form-control", "placeholder": "Password1"}),
        # }





class LoginForm(forms.Form):

    username = forms.CharField(max_length=255, widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())




class ProfileUpdateForm(forms.ModelForm):

    #email = forms.EmailField()

    class Meta:
        model = User
        fields = ["bio" ,"username", "image"]

        widgets = {
            "bio": forms.Textarea(attrs={"style": "background-color: lightgrey", "rows": "5"}),
            'username': forms.TextInput(attrs={'style': 'background-color: lightgrey'}),
        }



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content", "image"]

        widgets = {
            "content": forms.Textarea(attrs={"style": "background-color: lightgrey"}),
            "image": forms.ClearableFileInput(attrs={"style": "background-color: lightgrey"})
        }

