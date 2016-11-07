from django import forms
from .models import Mirnas
from .models import Tissues
from .models import Species

# from .models import MirnaForm

class FPKMForm(forms.Form):
    # your_name = forms.CharField(label='Your fdgfdgname', max_length=100) #FormField
    CHOICES = (('A','1 '),
               ('B','2'),
               ('C','3'),
               ('D','4'),)
    FPKM_threshold = forms.ChoiceField(choices=CHOICES) #Variable name html - pretty weird

class MirnaForm(forms.Form):
    # or with some filter applied
    mirnas = forms.ModelChoiceField(queryset=Mirnas.objects.all(), to_field_name="mirna_name"
                                    , empty_label="Choose your miRNA")
class TissueForm(forms.Form):
    # or with some filter applied
    tissues = forms.ModelChoiceField(queryset=Tissues.objects.all(), to_field_name="tissue_name"
                                    , empty_label="Choose your tissue")
class SpeciesForm(forms.Form):
    # or with some filter applied
    Species = forms.ModelChoiceField(queryset=Species.objects.all(), to_field_name="common_name"
                                     , empty_label="Choose your Species")


#widget=forms.CheckboxSelectMultiple()

# class MirnaForm(ModelForm):
#     class Meta:
#         model = Mirnas
#         fields = ['mirna_name']