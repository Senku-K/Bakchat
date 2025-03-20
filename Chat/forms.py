from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Message, UserProfile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)
    display_name = forms.CharField(max_length=50, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('display_name',)

class MessageForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'message-input',
            'placeholder': 'Type your message...',
            'autocomplete': 'off'
        })
    )

    class Meta:
        model = Message
        fields = ('content',)

