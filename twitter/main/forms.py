from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from main.models import UserProfile
from main.models import Tweet


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "password", "first_name", "last_name",)
        exclude = ("is_staff", "password", "is_active", "is_superuser", "last_login", "date_joined",)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
#        fields = ("username", "email", "password1", "password2", "first_name", "last_name")
        exclude = ("user", "followin",)


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        #exclude = ("auth",)


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "first_name", "last_name",)


def save(self, commit=True):
    user = super(UserCreateForm, self).save(commit=False)
    user.first_name = self.cleaned_data["first_name"]
    user.last_name = self.cleaned_data["last_name"]
    user.email = self.cleaned_data["email"]
    if commit:
        user.save()
    return user


class RegistrationForm(ModelForm):
    username = forms.CharField(label=(u'User Name'))
    email = forms.EmailField(label=(u'Email Address'))
    password = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))
    password1 = forms.CharField(label=(u'Verify Password'), widget=forms.PasswordInput(render_value=False))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
                User.objects.get(username=username)
        except User.DoesNotExist:
                return username
        raise forms.ValidationError("That username is already taken, please select another")

    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['password1']:
                raise forms.ValidationError("The passwords did not match. Please try again")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label=(u'User Name'))
    password = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))
