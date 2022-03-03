from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user



class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title','category','text','image')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder' :'Title','class':'form-group row','class':'form-control','style':'max-width:835px'}),
            'text': forms.Textarea(attrs={'placeholder' :'Text','class':'form-control'}),
            'category': forms.Select(attrs={'class':'form-control','style':'max-width:835px'}),
            'image':forms.FileInput(attrs={'class':'form-control','style':'max-width:835px'})
            }