from django import forms

class CreatNewPerson(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    age = forms.IntegerField(label="Age")
    gender = forms.ChoiceField(label="Gender", choices=(('Male', 'Male'),('Female', 'Female'),('Undefined', 'Undefined')))
    personalheight = forms.IntegerField(label="Height")
    personalweight = forms.IntegerField(label="Weight")

class SwitchPerson(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
