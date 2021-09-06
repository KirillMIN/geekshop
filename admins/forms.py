from users.forms import UserRegistrationForm, UserProfileForm
from users.models import User
from django import forms


class UserAdminRegistrationForm(UserRegistrationForm):

    class Meta:
        image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)
        model = User
        fields = ('username', 'email', 'image', 'first_name', 'last_name', 'password1', 'password2')


class UserAdminProfileForm(UserProfileForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': False}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'readonly': False}))
