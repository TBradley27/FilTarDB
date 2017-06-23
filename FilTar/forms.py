from django import forms
from .models import *

# from .models import MirnaForm

class TPMForm(forms.Form):
    CHOICES = ((0,'0'),
               (1,'1'),
               (2,'2'),
               (3,'3'),
               (4,'4'),)
    TPM_threshold = forms.ChoiceField(choices=CHOICES) #Variable name html - pretty weird

class MirnaForm(forms.Form):
    mirna = forms.ModelChoiceField(queryset=Mirnas.objects.all(), to_field_name="name"
                                    , empty_label="Choose your miRNA")
class TissueForm(forms.Form):

    Tissue = forms.ModelChoiceField(queryset=Tissues.objects.all(), to_field_name="name"
                                    , empty_label="Choose your tissue or cell line")
class SpeciesForm(forms.Form):
    CHOICES = (('9606','Human'),
               ("10090","Mouse"),)
    Species  = forms.ChoiceField(choices=CHOICES)

class AlgorithmForm(forms.Form):
    CHOICES = (('TargetScan7','TargetScan7'),
               ('miRanda','miRanda'),
               ('PITA','PITA'),)
    Algorithm = forms.ChoiceField(choices=CHOICES)

