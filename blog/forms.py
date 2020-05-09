from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Profile, Image, Comment
from django.forms import inlineformset_factory


class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'cover_photo',
            'title',
            'body',
            'status',
            'restrict_comments',
        ]

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'cover_photo',
            'title',
            'body',
            'status',
            'restrict_comments',
        ]

ImageFormSet = inlineformset_factory(Post, Image, extra=3, fields=('image',))


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]


class UserLoginForm(forms.Form):
    username = forms.CharField(label="")
    password = forms.CharField(label="", widget=forms.PasswordInput)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'bio',
            'phone_number',
            'location',
            'birth_date',
            'photo',
        ]

class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]

class CommentForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Text goes here!',
            'rows': '4',
            'cols': '50',
        }
    ))
    class Meta:
        model = Comment
        fields = [
            'content',
        ]