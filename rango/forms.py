from django import forms
from django.contrib.auth.models import User
from rango.models import Page, UserProfile

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length = 128, help_text = "Enter the page title.")
    url = forms.URLField(max_length = 200, help_text = "Enter the URL of the page.")
    views = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)

    class Meta:
        model = Page
        fields = ('title', 'url', 'views')

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get('url')

        # ensure URL starts with http:// or https://
        if url and not (url.startswith('http://') or url.startswith('https://')):
            url = 'http://' + url
            cleaned_data['url'] = 'http://' + url
        return cleaned_data
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')