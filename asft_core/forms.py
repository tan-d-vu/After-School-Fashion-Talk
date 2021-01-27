from django import forms
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from asft_core.models import Profile, Message
from . import brand_set

class ProfileForm(forms.ModelForm):
    picture = forms.ImageField(required=False)
    bio = forms.CharField(required=False, widget=forms.Textarea())

    favorite_designers= forms.TypedMultipleChoiceField( 
                             choices = brand_set.brand_choice, 
                             coerce = int, 
                             widget=forms.CheckboxSelectMultiple(),
                             required = True,
                             )     
    class Meta:
        model = Profile
        exclude = ('user', 'username', )

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('sender', 'reciever', 'created_at')
    