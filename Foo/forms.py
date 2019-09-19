from django import forms
from .models import *
from dal import autocomplete
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField

# from .models import MirnaForm

class TPMForm(forms.Form):
    TPM_threshold = forms.DecimalField(initial=0,min_value=0,max_value=1000,decimal_places=3,max_digits=8,
                                       label= "Select a TPM Threshold",
                                       widget = forms.NumberInput(attrs={'step': 1.0}))

class GeneForm(forms.Form):
    gene = forms.ModelChoiceField(queryset=Gene.objects.all(), to_field_name="name"
                                    , empty_label="Choose your gene (optional)", required=False, widget=forms.TextInput)

class TissueForm(forms.Form):

    Tissue = forms.ModelChoiceField(queryset=Tissues.objects.all(), to_field_name="name"
                                    , empty_label="Choose your tissue or cell line")

class SpeciesForm(forms.Form):
    CHOICES = (('9606','Human'),
               ("10090","Mouse"),)
    Species  = forms.ChoiceField(choices=CHOICES)

class AlgorithmForm(forms.Form):
    CHOICES = (('contextpp','TargetScan7'),
               ('miRanda','miRanda'))
    Algorithm = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple,
                                          label="Select one or multiple miRNA target prediction algorithms",
                                          error_messages={'required': 'Please select at least one algorithm'})

CHOICES = (('9606', 'Human'),
           ('10090', 'Mouse'))

class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.common_name

class ExampleFKForm(forms.ModelForm):

    continent = MyModelChoiceField(queryset=Species.objects.all(), empty_label="Select a species", label="")

    tissues = forms.ModelChoiceField(queryset=Tissues.objects.all(), required=True, empty_label=None,
                                     label = "",
                                     widget=autocomplete.ModelSelect2(url='/tissues-autocomplete',
                                                                      attrs={
                                                                          'data-placeholder': 'Type a tissue name (required)',
                                                                      },
                                                                      forward=['continent']),
                                     error_messages={'required': 'Please select a tissue or cell line'})

    gene = forms.ModelChoiceField(queryset=Gene.objects.all(), required=False, empty_label=None,
                                    label="",
                                     widget=autocomplete.ModelSelect2(url='/gene-autocomplete',
                                                                      attrs={
                                                                          'data-placeholder': 'Type a gene name',
                                                                      },
                                                                    forward=['continent']))
    class Meta:

        model = ExampleFK
        labels = {"test": "" }
        fields = ('continent','tissues','test','gene')
        widgets = {
            'test': autocomplete.ModelSelect2(url='/mirna-autocomplete',
            attrs = {
                'data-placeholder': 'Type a miRNA name'
            }
            ,forward=['continent']),
        }

    def clean(self):
        if not (self.cleaned_data['gene'] or self.cleaned_data['test']):
            raise ValidationError("You cannot leave both the miRNA and the gene forms empty")


