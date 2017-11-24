from django import forms
from .models import *
from dal import autocomplete
from decimal import Decimal

# from .models import MirnaForm

class TPMForm(forms.Form):
    # CHOICES = ((0,'0'),
    #            (1,'1'),
    #            (2,'2'),
    #            (3,'3'),
    #            (4,'4'),)
    TPM_threshold = forms.DecimalField(initial=0,min_value=0,max_value=1000,decimal_places=3,max_digits=8) #Variable name html - pretty weird


class GeneForm(forms.Form):
    gene = forms.ModelChoiceField(queryset=Gene.objects.all(), to_field_name="name"
                                    , empty_label="Choose your gene (optional)", required=False, widget=forms.TextInput)

class TissueForm(forms.Form):

    Tissue = forms.ModelChoiceField(queryset=Tissues.objects.all(), to_field_name="name"
                                    , empty_label="Choose your tissue or cell line")

class LocationForm(forms.ModelForm):

    species = forms.ModelChoiceField(Species.objects.all(), empty_label=None)

    class Meta:
        model = Location
        fields = ['species', 'miRNA', 'tissue']
        widgets = {
            'miRNA': autocomplete.ModelSelect2(url='filtar:select2_fk',
                                              attrs={
                                                  'data-placeholder': 'Type a miRNA name',
                                                  'data-minimum-input-length': 2
                                              })
        }

class SpeciesForm(forms.Form):
    CHOICES = (('9606','Human'),
               ("10090","Mouse"),)
    Species  = forms.ChoiceField(choices=CHOICES)

class AlgorithmForm(forms.Form):
    CHOICES = (('contextpp','TargetScan7'),
               ('miRanda','miRanda'),
               ('PITA', 'PITA'))
    Algorithm = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple)


CHOICES = (('9606', 'Human'),
           ('10090', 'Mouse'))

class ExampleFKForm(forms.ModelForm):

    continent = forms.ChoiceField(choices=CHOICES)

    tissues = forms.ModelChoiceField(queryset=Tissues.objects.all(), required=True, empty_label=None,
                                     widget=autocomplete.ModelSelect2(url='filtar/tissues-autocomplete',
                                                                      attrs={
                                                                          'data-placeholder': 'Type a tissue name',
                                                                      },
                                                                      forward=['continent']))

    gene = forms.ModelChoiceField(queryset=Gene.objects.all(), required=False, empty_label=None,
                                     widget=autocomplete.ModelSelect2(url='filtar/gene-autocomplete',
                                                                      attrs={
                                                                          'data-placeholder': 'Type a gene name',
                                                                      },
                                                                      forward=['continent']))
    class Meta:

        model = ExampleFK
        fields = ('continent','test','tissues','gene')
        widgets = {
            'test': autocomplete.ModelSelect2(url='filtar/country-autocomplete',
            attrs = {
                'data-placeholder': 'Type a miRNA name',
                'data-minimum-input-length': 2
            }
            ,forward=['continent']),
        }

    class Media:
        js = (
            'linked_data.js',
        )






# class TissuesFKForm(forms.ModelForm):
#
#     foo = forms.ChoiceField(choices=CHOICES2)
#
#     # tissues = forms.ModelChoiceField(Tissues.objects.all(), empty_label=None, to_field_name='name')
#     #             # widget=autocomplete.ModelSelect2(url='filtar/tissues-autocomplete', forward=['continent']))
#
#     class Meta:
#         model = Tissues
#         fields = ('foo','test')
#         widgets = {
#             'test': autocomplete.ModelSelect2(url='filtar/tissues-autocomplete',
#             attrs = {
#                 # 'data-placeholder': 'Type a miRNA name',
#                 # 'data-minimum-input-length': 2
#             }
#             ,forward=['foo']),
#
#             # 'tissues': autocomplete.ModelSelect2(url='filtar/tissues-autocomplete',
#             # attrs={
#             #     'data-placeholder': 'Type a miRNA name',
#             #     'data-minimum-input-length': 2
#             # }
#             # ,forward=['continent'])
#         }
#
#     class Media:
#         js = (
#             'linked_data.js',
#         )


# class TForm(forms.ModelForm):
#     class Meta:
#         model = TModel
#         fields = ('name','test')

# class ExampleForm(forms.ModelForm):
#     class Meta:
#         model = Example
#         fields = ('test',)
#         widgets = {
#             'test': autocomplete.ModelSelect2(
#                 'filtar:select2_many_to_many_autocomplete'
#             )
#         }

# class ExampleFKForm(forms.ModelForm):
#     CHOICES = (('contextpp','Apple'),
#                ('miRanda','Banana'),
#                ('PITA', 'Orange'))
#     continent = forms.ChoiceField(choices=CHOICES)
#
#     class Meta:
#         model = ExampleFK
#         fields = ('test',)
#         widgets = {
#             'test': autocomplete.ModelSelect2(url='filtar:select2_fk',
#                                               attrs={
#                                                   'data-placeholder': 'Type a miRNA name',
#                                                   'data-minimum-input-length' : 2
#                                               }, forward=['continent'])
#         }

    # def __init__(self, *args, **kwargs):
    #     super(LocationForm, self).__init__(*args, **kwargs)
    #     self.fields['tissue'].empty_label = "ggggg"
    #     # following line needed to refresh widget copy of choice list
    #     self.fields['tissue'].widget.choices = self.fields['tissue'].choices

    # def __init__(self, *args, **kwargs):
    #     super(ThingForm, self).__init__(*args, **kwargs)
    #     self.fields['species'].empty_label = None

        # widgets = {
        #     'species': forms.Select(attrs=)
        # }

# class TissueForm(forms.Form):
#     def __init__(self, tissue_choices, *args, **kwargs):
#         super(TissueForm, self).__init__(*args, **kwargs)
#         self.fields['TissueForm'].choices = tissue_choices
#
#     TissueForm = forms.ChoiceField(choices=(), required=True)

# class MirnaForm(forms.Form):
#     mirna = forms.ModelChoiceField(queryset=Mirnas.objects.all(), to_field_name="name"
#                                     , empty_label="Choose your miRNA (optional)", required=False)