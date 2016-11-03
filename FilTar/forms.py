from django import forms
from .models import Mirnas
# from .models import MirnaForm

class SomeForm(forms.Form):
    # your_name = forms.CharField(label='Your fdgfdgname', max_length=100) #FormField
    CHOICES = (('a','a'),
               ('b','b'),
               ('c','c'),
               ('d','d'),)
    miRNAs = forms.ChoiceField(choices=CHOICES) #Variable name html - pretty weird

class MyForm(forms.Form):
    # or with some filter applied
    mirnas = forms.ModelChoiceField(queryset=Mirnas.objects.all(), to_field_name="mirna_name"
                                    , empty_label="Choose your miRNA")


#widget=forms.CheckboxSelectMultiple()

# class MirnaForm(ModelForm):
#     class Meta:
#         model = Mirnas
#         fields = ['mirna_name']