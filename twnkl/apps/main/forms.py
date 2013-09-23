from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.forms.widgets import TextInput, PasswordInput, Textarea, FileInput, Select, CheckboxInput, CheckboxSelectMultiple, HiddenInput, MultipleHiddenInput
from django.forms.models import ModelMultipleChoiceField
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from twnkl.apps.main.models import Photo, PhotoGroup, Tag

class MyMultipleHiddenInput(MultipleHiddenInput):
    def render(self, name, value, **kwargs):
        return super(MyMultipleHiddenInput, self).render(name, value, **kwargs)

class BetterCheckbox(CheckboxSelectMultiple):
    def __init__(self, *args, **kwargs):
        return super(BetterCheckbox, self).__init__(*args, **kwargs)

    def render(self, *args, **kwargs):
        output = super(BetterCheckbox, self).render(*args, **kwargs)
        return mark_safe("<label>Enter groups this photo should be a part of:</label><p>" + output.replace(u'<ul>', u'').replace(u'<li>', u'') + "</p>")


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

class MyModelMultipleChoiceField(ModelMultipleChoiceField):
    def clean(self, value):
        pks = []
        for tag_text in value:
            tag, created = Tag.objects.get_or_create(text=tag_text)
            tag.save()
            pks.append(tag.pk)
        return super(MyModelMultipleChoiceField, self).clean(pks)

class PhotoUploadForm(forms.ModelForm):
    tags = MyModelMultipleChoiceField(Tag.objects.all())
 
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(PhotoUploadForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = ""
        self.fields['name'].widget = TextInput(attrs={'placeholder':'Name',
                                                      'class':'form-control',
                                                      'required':''})
        self.fields['tags'].widget = MyMultipleHiddenInput()
        self.fields['tags'].label = "" 
        self.fields['tags'].help_text = ""
        self.fields['tags'].required = False
        self.fields['image'].widget = FileInput(attrs={'style':'display:none',
                                                       'required':''})
        self.fields['image'].label = ""
        self.fields['image'].help_text = ""
        self.fields['groups'].widget = BetterCheckbox(attrs={'required':''},choices=[(o.id, str(o.name)) for o in PhotoGroup.objects.filter(owner__username=user)])
        self.fields['groups'].label = ""
        self.fields['groups'].help_text = ""
        self.fields['groups'].required = True
        #self.fields['loc'].widget = TextInput(attrs={'placeholder': 'Where?',
        #                                             'class':'form-control'})
        #self.fields['loc'].label = ""

    class Meta:
        model = Photo
        exclude = ('owner','loc')

class PhotoUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(PhotoUpdateForm, self).__init__(*args, **kwargs)
        self.fields['tags'].widget = TextInput(attrs={'placeholder':'Enter Tags',
                                                      'class':'form-control'})
        self.fields['tags'].label = "" 
        self.fields['tags'].help_text = ""
        self.fields['name'].label = ""
        self.fields['name'].widget = TextInput(attrs={'placeholder':'Name',
                                                      'class':'form-control'})
        self.fields['groups'].widget = BetterCheckbox(choices=[(o.id, str(o.name)) for o in PhotoGroup.objects.filter(owner__username=user)])
        self.fields['groups'].label = ""
        self.fields['groups'].help_text = ""

    class Meta:
        model = Photo
        exclude = ('owner', 'loc', 'image',)
