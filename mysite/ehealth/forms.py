from django import forms

class CreatNewPerson(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    age = forms.IntegerField(label="Age")
    gender = forms.CharField(label="Gender", max_length=10)
    personalheight = forms.IntegerField(label="Height")
    personalweight = forms.IntegerField(label="Weight")
    check = forms.BooleanField()
