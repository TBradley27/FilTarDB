from django import forms
from .models import Mirnas


class SomeForm(forms.Form):
    # your_name = forms.CharField(label='Your fdgfdgname', max_length=100) #FormField
    CHOICES = (('a','a'),
               ('b','b'),
               ('c','c'),
               ('d','d'),)
    miRNAs = forms.ChoiceField(choices=CHOICES) #Variable name html - pretty weird


#widget=forms.CheckboxSelectMultiple()

# class MirnaForm(ModelForm):
#     class Meta:
#         model = Mirnas
#         fields = ['mirna_name']