from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


'''

This UserRegisterForm is an extension of the built-in django UserCreationForm. The UserCreationForm contains built-in 
features such as the username, password1 and password2 (to prevent typos while entering password) which comes
along with built-in authentication such as hashing the password(i.e making it appear as dots while typing to ensure it
cant be peaked at) and validating it (by ensuring that a password for example has a Capital letter, a small letter etc.)

So I am getting / extending all these functionalities of the built-in UserCreationForm into the 
new form (UserRegisterForm) that I am creating  by writing this line --> class UserRegisterForm(UserCreationForm):

We are adding an email section to our new form (UserRegisterForm) using the built-in django's EmailField as there 
is no built-in email section in the UserCreationForm. The django's built-in email section comes with built-in
authentication system so we need not worry about the logic part of the authentication

In summary, model = User tells Django that this form is based on the User model, and it should pull these fields from that 
model. The form will allow users to create or update User instances in the database as the data from this form is stored in the user database

The model attribute within the meta class tells django which database table I would want to associate the form with and 
fields=['username', 'email', 'password1', 'password2']: Specifies which fields from the form should map to fields in the 
User model. While password1 and password2 are form fields for user input and not physically present int he user mode, 
they translate password1/map while the form is being saved to User.password when form.save() is performed in the view

User model with the following fields:
- username   
- password (hashed)
- email
- first_name
- last_name
- is_active
- date_joined


'''


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image','age','height','weight']



