from django import forms
from accounts.models import Address,User

class RegisterForm(forms.Form):
    phone_number = forms.CharField(max_length=12)

class RegisterVerifyForm(forms.Form):
    code = forms.CharField(max_length=6)


class UserInformation(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','phone_number','birthday','email')


class EditAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('neighbourhood','state','formatted_address','plaqe','floor','postal_code')




