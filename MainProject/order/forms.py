from django import forms

from accounts.models import User


class ReceiverForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('phone_number', 'first_name', 'last_name')

        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'})
        }
        labels = {
            'phone_number': 'شماره تلفن',
            'last_name': 'نام خانوادگی',
            'first_name': 'نام'
        }

    def validate_unique(self):
        pass


class CopounForm(forms.Form):
    code = forms.CharField(max_length=255)
