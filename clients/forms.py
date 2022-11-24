from django import forms
from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import *


class AddDoctorForm(ModelForm):
    class Meta:
        model = ServiceWorkers
        fields = ['name', 'schedule_from', 'schedule_to', 'speciality']

    def __init__(self, *args, **kwargs):
        super(AddDoctorForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Ім\'я'
        # self.fields['location'].widget.attrs['placeholder'] = 'Номер кабінету'
        self.fields['schedule_from'].widget.attrs['placeholder'] = 'Від'
        self.fields['schedule_to'].widget.attrs['placeholder'] = 'до'
        self.fields['schedule_from'].widget.attrs['type'] = 'number'
        self.fields['schedule_to'].widget.attrs['type'] = 'number'
        self.fields['speciality'].widget.attrs['placeholder'] = 'Спеціальність'

        # self.fields['location'].widget.attrs['list'] = 'cabinets'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CreateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CreateUserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['style'] = 'margin-bottom: 10px;'
        self.fields['password'].widget.attrs['style'] = 'margin-bottom: 10px;'
        self.fields['username'].widget.attrs['placeholder'] = 'Логін'
        self.fields['email'].widget.attrs['placeholder'] = 'Електронна пошта'
        self.fields['password'].widget.attrs['placeholder'] = 'Пароль'


# class EditRecipeForm(forms.Form):
#     name = forms.CharField(label='Назва', max_length=255, required=True)
#     description = forms.CharField(label='Опис', max_length=255, required=True)
#
#     def __init__(self, *args, **kwargs):
#         super(EditRecipeForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs['class'] = 'form-control'


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Логін', max_length=100, required=True)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(), required=True, max_length=100)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['style'] = 'margin-bottom: 10px;'
        self.fields['password'].widget.attrs['style'] = 'margin-bottom: 10px;'
        self.fields['username'].widget.attrs['placeholder'] = 'Логін'
        self.fields['password'].widget.attrs['placeholder'] = 'Пароль'


class AddManagerForm(ModelForm):
    class Meta:
        model = Manager
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(AddManagerForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Ім\'я'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class AddAdminForm(ModelForm):
    class Meta:
        model = Administrator
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(AddAdminForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Ім\'я'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class AddCabinetForm(ModelForm):
    class Meta:
        model = Location
        fields = ['cabinet_number']

    def __init__(self, *args, **kwargs):
        super(AddCabinetForm, self).__init__(*args, **kwargs)
        self.fields['cabinet_number'].widget.attrs['placeholder'] = 'Номер кабінету'


class AddProcedureForm(ModelForm):
    class Meta:
        model = Procedure
        fields = ['name', 'name_of_speciality', 'duration']

    def __init__(self, *args, **kwargs):
        super(AddProcedureForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Назва'
        self.fields['name_of_speciality'].widget.attrs['placeholder'] = 'Назва спеціальності'
        self.fields['duration'].widget.attrs['placeholder'] = 'Тривалість'


class AddAppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ['name_of_procedure', 'hour']

    def __init__(self, *args, **kwargs):
        super(AddAppointmentForm, self).__init__(*args, **kwargs)
        self.fields['name_of_procedure'].widget.attrs['placeholder'] = 'Назва процедури'
        self.fields['hour'].widget.attrs['placeholder'] = 'Година'
