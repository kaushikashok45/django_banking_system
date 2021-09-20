from django import forms

class InputForm(forms.Form):
    Amount = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder':'Type an amount','style':'font-size:large;','class':'form-control'}))

