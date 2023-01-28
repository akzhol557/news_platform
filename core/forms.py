from dataclasses import field
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils import timezone


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Придумайте пароль', 'class': 'form-control d-block w-100'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Подтвердите пароль', 'class': 'form-control d-block w-100'})

    class Meta:
        model = NewUser
        fields = ["username", "email", "password1", "password2", "name", "phone_number"]

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Логин', 'class': 'form-control d-block w-100'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Почта', 'class': 'form-control d-block w-100'}),
            'name': forms.TextInput(attrs={'placeholder': 'ФИО', 'class': 'form-control d-block w-100'}),
            'phone_number': forms.TextInput(
                attrs={'placeholder': 'Номер телефона', 'class': 'form-control d-block w-100'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Заголовок', 'class': 'form-control d-block w-100'}),
            'password2': forms.PasswordInput(
                attrs={'placeholder': 'Подтвердите пароль', 'class': 'form-control d-block w-100'}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(max_length=155,
                               widget=forms.TextInput(attrs={'class': 'text-center', 'placeholder': 'Username'}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'text-center', 'placeholder': 'Password'}))


class CreateEditNewsForm(forms.ModelForm):

    class Meta:
        model = News
        fields = ["title", "information", 'category', 'image_1', "date", "author",]
        title = {
            'title': 'Тема',
            'information': 'Контент',
            'image_1': 'Изображение',
        }

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Заголовок', 'class': 'form-control'}),
            'image_1': forms.FileInput(attrs={'accept': 'image/*', 'id': 'image_1', 'class': 'input input__file',}),
            'information': CKEditorUploadingWidget(),
            'category': forms.CheckboxSelectMultiple(),
            'author': forms.HiddenInput(),
            'date': forms.HiddenInput(),
        }


class SearchNewsForm(forms.ModelForm):
    
    class Meta:
        model = News
        fields = ['category', "author",]
        title = {
            'date': 'Дата',
            'author': 'Автор',
        }

        widgets = {
            'category': forms.CheckboxSelectMultiple(),
            'author': forms.CheckboxSelectMultiple(),
        }
