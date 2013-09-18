from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.forms.widgets import TextInput, PasswordInput, Textarea, FileInput, Select
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import TextInput, PasswordInput
from django.contrib.auth.models import User
from twnkl.apps.main.models import Photo

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username",)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget = TextInput(attrs={'placeholder':'First Name',
                                                          'class':'form-control',
                                                          'required':''})
        self.fields['last_name'].widget = TextInput(attrs={'placeholder':'Last Name',
                                                          'class':'form-control',
                                                          'required':''})
        self.fields['email'].widget = TextInput(attrs={'placeholder':'Email Address',
                                                          'class':'form-control',
                                                          'type':'email',
                                                          'required':''})
        self.fields['username'].widget = TextInput(attrs={'placeholder':'Username',
                                                          'class':'form-control',
                                                          'required':''})
        self.fields['password1'].widget = PasswordInput(attrs={'placeholder':'Password',
                                                          'class':'form-control',
                                                          'required':''})
        self.fields['password2'].widget = PasswordInput(attrs={'placeholder':'Confirm Password',
                                                          'class':'form-control',
                                                          'required':''})

class MyAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(MyAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = TextInput(attrs={'placeholder': 'Username',
                                                          'class': 'form-control',
                                                          'required':''})
        self.fields['password'].widget = PasswordInput(attrs={'placeholder': 'Password',
                                                          'class': 'form-control',
                                                          'required':''})

class PhotoUploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PhotoUploadForm, self).__init__(*args, **kwargs)
        self.fields['tags'].widget = TextInput(attrs={'placeholder':'Enter tags',
                                                      'class':'form-control'})
        self.fields['tags'].label = "" 
        self.fields['tags'].help_text = ""
        self.fields['image'].widget = FileInput(attrs={'style':'display:none'})
        self.fields['image'].label = ""
        self.fields['image'].help_text = ""
        self.fields['group'].widget = Select() 
        self.fields['group'].label = ""
        self.fields['group'].help_text = ""

    class Meta:
        model = Photo
        exclude = ('owner','loc',)
