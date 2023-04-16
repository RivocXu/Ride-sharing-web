from datetime import datetime


from django import forms
from captcha.fields import CaptchaField
from django.forms import ModelForm
from django.utils import timezone

from rideservice.models import RideUser, Vehicle, Ride


class UserForm(forms.Form):
    username = forms.CharField(label="username", max_length=128,widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='verification code')

class RegisterForm(forms.Form):
    gender = (
        ('male', 'male'),
        ('female', 'female'),
    )
    username = forms.CharField(label="username", max_length=128,widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    repeat_password = forms.CharField(label="repeat_password", max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label = "emailaddress",widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label="sex",choices=gender)
    captcha = CaptchaField(label='verification code')

class SearchForm(ModelForm):

    capacity = forms.IntegerField(label="capacity",widget=forms.TextInput(attrs={'class': 'form-control','readonly':'readonly'}),required=False)
    type = forms.CharField(label="type", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control','readonly':'readonly'}),required=False)
    otherInfo = forms.CharField(label="otherInfo", max_length=256,widget=forms.TextInput(attrs={'class': 'form-control','readonly':'readonly'}),required=False)

    class Meta:
        model = Vehicle
        fields = ['capacity', 'type', 'otherInfo']


class EditForm(ModelForm):
    gender = (
        ('male', 'male'),
        ('female', 'female'),
    )
    name = forms.CharField(label="username", max_length=128,widget=forms.TextInput(attrs={'class': 'form-control','readonly':'readonly'}))
    email = forms.EmailField(label = "emailaddress",widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label="sex",choices=gender)


    class Meta:
        model = RideUser
        fields = ['name', 'email', 'sex']

    #def __init__(self,*args,**kwargs):
        #super(EditForm,self).__init__(*args,**kwargs)

class EditCarForm(ModelForm):
    type = forms.CharField(label='type', max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    license_num = forms.CharField(label='license_num', max_length=128,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    capacity = forms.CharField(label='capacity', max_length=128,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    sInfo = forms.CharField(label='otherInfo', max_length=128,
                                widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Vehicle
        fields = ['type', 'license_num', 'capacity', 'otherInfo']



class beDriverForm(ModelForm):

    class Meta:
        model = Vehicle
        fields = ['type','license_num','capacity','otherInfo']

    type = forms.CharField(label='type', max_length=128,widget=forms.TextInput(attrs={'class': 'form-control'}))
    license_num = forms.CharField(label='license_num', max_length=128,widget=forms.TextInput(attrs={'class': 'form-control'}))
    capacity = forms.CharField(label='capacity', max_length=128,widget=forms.TextInput(attrs={'class': 'form-control'}))
    otherInfo = forms.CharField(label='otherInfo', max_length=128,widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)


class UserRequestForm(ModelForm):
    destination = forms.CharField(label = 'destination',widget=forms.TextInput(attrs={'class': 'form-control'}))
    arrival_time = forms.DateTimeField(label = 'Arrival time',


                                       input_formats=['%Y-%m-%d %H:%M'],
                                       widget=forms.DateTimeInput(
                                           format='%Y-%m-%d %H:%M',
                                           attrs={'class': 'form-control'}))
    capacity = forms.IntegerField(label='Number of your party',widget=forms.NumberInput(attrs={'class': 'form-control'}))
    vehicle_type = forms.CharField(label='vehicle_type', required = False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    special_request = forms.CharField(label='special_request', required = False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    is_Share = forms.BooleanField(label = 'is_Share',required=False,widget=forms.CheckboxInput())

    class Meta:
        model = Ride
        fields = ['destination', 'arrival_time', 'capacity', 'vehicle_type', 'special_request', 'is_Share']

    def __init__(self, *args, **kwargs):
        super(UserRequestForm, self).__init__(*args, **kwargs)

        self.initial["arrival_time"] = timezone.now

class UserSearchForm(forms.Form):

    destination = forms.CharField(label = 'destination',max_length=128,widget=forms.TextInput(attrs={'class': 'form-control'}))
    early_time = forms.DateTimeField(label = 'Early time',
                                    required=False,
                                    input_formats=['%Y-%m-%d %H:%M'],
                                    widget=forms.DateTimeInput(
                                        format='%Y-%m-%d %H:%M',
                                        attrs={'class': 'form-control'}))
    late_time = forms.DateTimeField(label = 'Late time',
                                    required=False,

                                    input_formats=['%Y-%m-%d %H:%M'],
                                    widget=forms.DateTimeInput(
                                        format='%Y-%m-%d %H:%M',
                                        attrs={'class': 'form-control'}))
    number_you = forms.IntegerField(label="Number of your party(At least 1)",widget=forms.NumberInput(attrs={'class': 'form-control'}),required=False)

    def __init__(self, *args, **kwargs):
        super(UserSearchForm, self).__init__(*args, **kwargs)

        self.initial["number_you"] = 1  # 方法2
        self.initial["early_time"] = timezone.now
        self.initial["late_time"] = timezone.now
