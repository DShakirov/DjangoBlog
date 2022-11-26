from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from blog.models import Comment, Post



class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form_control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form_control'}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form_control'}))
    email = forms.EmailField(label='email', widget=forms.EmailInput(attrs={'class': 'form_control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form_control'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form_control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CommentForm(forms.ModelForm):

    name = forms.CharField(label ='Name', widget= forms.TextInput(attrs={'class': 'form_control'}))
    email = forms.EmailField(label='email', widget=forms.EmailInput(attrs={'class': 'form_control'}))
    content = forms.CharField(label='Комментарий', widget=forms.Textarea(attrs={'class': 'form_control'}))

    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']


class UserAddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'photo', 'category', 'tags']
        widgets = {'title': forms.TextInput(attrs={'class':'form-control'})},
        {'text': forms.Textarea(attrs={'class': 'form-control', 'rows':5, })},
        {'category': forms.Select(attrs={'class': 'form-control'})}

        def get_title(self):
            title = self.cleaned_data['title']
            return title

