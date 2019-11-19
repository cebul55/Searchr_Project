from django import forms
from registration.models import UserModel


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ('username', 'email_address', 'first_name', 'last_name', 'password')

# todo modify registration form to have: username, mail, password, first last name
# https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
