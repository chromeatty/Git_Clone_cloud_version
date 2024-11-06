from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import User, Profile

class SignUpForm(UserCreationForm):
    # Adding a user_type field with choices defined in the User model
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES, 
                                  widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('name', 'email', 'username', 'user_type', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        # Applying custom attributes to various fields
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Full Name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        #self.fields['user_type'].widget.attrs.update({'class': 'form-control'})
        
        # Password fields customization
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['contact_info', 'service_areas', 'preferences', 'privacy_settings', 'latitude', 'longitude']

class UserLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, label='Remember Me')
    # put a placeholder for the username and password feilds
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')


        if username and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    "Please enter a correct username and password. Note that both fields may be case-sensitive."
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                "This account is inactive.",
                code='inactive',
            )
        
"""
class UserLoginOut(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, label='Remember Me')
    # put a placeholder for the username and password feilds
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')


        if username and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    "Please enter a correct username and password. Note that both fields may be case-sensitive."
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                "This account is inactive.",
                code='inactive',
            )
"""