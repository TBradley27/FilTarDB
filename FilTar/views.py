from django.views import generic
# from django.views.generic.edit import CreateView
from .models import Species
from .models import Mirnas
from .models import Contextpp
from .models import MiRanda
from .models import Experiments
from .models import PITA
from .models import ExpressionProfiles
from .forms import TPMForm
from .forms import MirnaForm
from .forms import TissueForm
from .forms import SpeciesForm
from .forms import AlgorithmForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.forms import ModelChoiceField
from itertools import chain
from django.db import connection
from collections import namedtuple
import decimal


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def getname(request):

    # if request.method == 'POST':
    #     form = SomeForm(request.POST)
    #     if form.is_valid():
    #         # picked = form.cleaned_data.get('picked')
    #         return HttpResponseRedirect('/thanks/')
    # else:
    #     form = SomeForm()
    # # return render(request, 'filtar/testing.html', {'form': form})

    if request.method == 'POST':
        form_Mirnas = MirnaForm(request.POST)
        form_species = SpeciesForm(request.POST)
        form_TPM = TPMForm(request.POST)
        form_tissue = TissueForm(request.POST)
        form_algorithm = AlgorithmForm(request.POST)

        if form_Mirnas.is_valid() and form_species.is_valid() and form_TPM.is_valid() and form_tissue.is_valid() and form_algorithm.is_valid():
             form_species = form_species.cleaned_data['Species']
             form_Mirnas = form_Mirnas.cleaned_data['mirna']
             form_TPM =  form_TPM.cleaned_data['TPM_threshold']
             form_tissue = form_tissue.cleaned_data['Tissue']
             form_algorithm = form_algorithm.cleaned_data['Algorithm']

             experiments = Experiments.objects.filter(species=form_species).filter(tissue=form_tissue).values()
             experiment_ID = experiments[0]['experiment_name']  # Change this

             if form_algorithm == 'TargetScan7':

                 scores = Contextpp.objects.filter(mirna=form_Mirnas
                                                   ).filter(
                     species=form_species)

                 # expression = ExpressionProfiles.objects.filter(experiments__experiment_name=experiment_ID) # This is very confusing - I don't think this line is doing anything at the moment

                 cursor = connection.cursor()
                 cursor.execute('''SELECT e.TPM, c.mirna_id, c.mrna_id, c.contextpp_score, c.UTR_START, c.UTR_END, c.Site_Type
                                  FROM contextpp c
                                  JOIN expression_profiles e
                                  ON c.mrna_id = e.mrnas_id
                                  AND c.mirna_id = %s
                                  AND c.Species = %s
                                  AND e.experiments_id = %s
                                  AND e.TPM >= %s''', [form_Mirnas, form_species, experiment_ID, form_TPM])
                 row = namedtuplefetchall(cursor)

                 tpm = []
                 mirna_id = []
                 mrna_id = []
                 contextpp_score = []
                 utr_start = []
                 utr_end = []
                 site_type = []
                 for x in range (0,len(row)):
                    # y.append(row[x].TPM)
                    tpm.append(str(row[x].TPM))
                    mirna_id.append((row[x].mirna_id))
                    mrna_id.append((row[x].mrna_id))
                    contextpp_score.append((row[x].contextpp_score))
                    utr_start.append((row[x].UTR_START))
                    utr_end.append((row[x].UTR_END))
                    site_type.append((row[x].Site_Type))


                    # contextpp_id.append(('')) #Dummy column because of weird column shift in output - weird

                 x = zip(mirna_id, mrna_id, utr_start, utr_end, site_type, contextpp_score, tpm)

                 # print(j)

                 return render(request, 'filtar/contextpptable.html', {'scores': scores, 'x':x} )

             elif form_algorithm == 'miRanda':

                 scores = MiRanda.objects.filter(mirna=form_Mirnas
                                                   ).filter(
                     species=form_species)

                 cursor = connection.cursor()
                 cursor.execute('''SELECT e.TPM, m.Mrnas, m.Mirnas, m.miranda_score, m.Start_pos, m.End_pos
                                                   FROM miRanda m
                                                   JOIN expression_profiles e
                                                   ON m.Mrnas = e.mrnas_id
                                                   AND m.Mirnas = %s
                                                   AND m.Species = %s
                                                   AND e.experiments_id = %s
                                                   AND e.TPM >= %s''',
                                [form_Mirnas, form_species, experiment_ID, form_TPM])
                 row = namedtuplefetchall(cursor)

                 tpm = []
                 Mirnas = []
                 Mrnas = []
                 miranda_score = []
                 start = []
                 end = []
                 for x in range(0, len(row)):
                     tpm.append(str(row[x].TPM))
                     Mirnas.append((row[x].Mirnas))
                     Mrnas.append((row[x].Mrnas))
                     miranda_score.append((row[x].miranda_score))
                     start.append((row[x].Start_pos))
                     end.append((row[x].End_pos))

                 x = zip(mirna_id, mrna_id, start, end, miranda_score, tpm)

                 return render(request, 'filtar/mirandatable.html', {'scores': scores, 'x': x})


             else:

                 scores = PITA.objects.filter(mirna=form_Mirnas
                                                 ).filter(
                     species=form_species)

                 cursor = connection.cursor()
                 cursor.execute('''SELECT e.TPM, p.Mrnas, p.Mirnas, p.PITA_score, p.UTR_START, p.UTR_END
                                                                    FROM PITA p
                                                                    JOIN expression_profiles e
                                                                    ON p.Mrnas = e.mrnas_id
                                                                    AND p.Mirnas = %s
                                                                    AND p.Species = %s
                                                                    AND e.experiments_id = %s
                                                                    AND e.TPM >= %s''',
                                [form_Mirnas, form_species, experiment_ID, form_TPM])
                 row = namedtuplefetchall(cursor)

                 tpm = []
                 Mirnas= []
                 Mrnas = []
                 PITA_score = []
                 start = []
                 end = []
                 for x in range(0, len(row)):
                     tpm.append(str(row[x].TPM))
                     Mirnas.append((row[x].Mirnas))
                     Mrnas.append((row[x].Mrnas))
                     PITA_score.append((row[x].PITA_score))
                     start.append((row[x].UTR_START))
                     end.append((row[x].UTR_END))

                 x = zip(Mirnas, Mrnas, start, end, PITA_score, tpm)

                 return render(request, 'filtar/pitatable.html', {'scores': scores, 'x': x})

    else:
        form_TPM = TPMForm()
        form_Mirnas = MirnaForm()
        form_tissue = TissueForm()
        form_species = SpeciesForm()
        form_algorithm = AlgorithmForm()

    return render(request, 'filtar/testing.html',{'form_Mirnas': form_Mirnas, 'form_species': form_species, 'form_TPM': form_TPM,
                                                  'form_algorithm': form_algorithm, 'form_tissue': form_tissue})

def contextpp(request):
    scores = Contextpp.objects.all()
    return render(request, 'filtar/contextpptable.html', {'scores': scores})

# def contextpp_table(request):
#     contextpp = Contextpp_Form()
#     return render(request, 'filtar/contextpptable.html', {'contextpp': contextpp})

    # return render_to_response('filtar/index.html', {'form':form },
    #     context_instance=RequestContext(request))

	# model = Mirnas
    #
	# template_name = 'filtar/index.html'
	# success_url = 'filtar/index.html'

class IndexView(generic.ListView):
	template_name = 'filtar/index.html'

	def get_queryset(self):
		return Species.objects.all()

class DetailView(generic.DetailView):
	model = Species
	template_name = 'filtar/detail.html'







# # from django.http import Http404
#
# from django.shortcuts import render, get_object_or_404
# # from django.http import HttpResponse
# from FilTar.models import Species
#
# def index(request):
# 	 all_species = Species.objects.all()
# 	 #template = loader.get_template('FilTar/index.html')
# 	 context = {	'all_species' : all_species, }
# 	 return render(request, 'filtar/index.html', context)
# # 	html = ()
# # 	for species in all_species:
# # 	     url = '/filtar/' + str(species.id) + '/'
# # 	     html += ('<a href="' + url + '">' + species.common_name + '</a><br>',)
#
#
# def detail(request, species_id):
# # 	try:
# # 		species = Species.objects.get(pk=species_id)
# # 	except Species.DoesNotExist:
# # 		raise Http404("Species does not exist")
# 	species = get_object_or_404(Species, pk=species_id)
# 	return render(request, 'filtar/detail.html', ({'species': species}) )
# # 	return HttpResponse("<h2>Details for Species id: " + str(species_id) + "</h2>")
#
#
#
# # 	return HttpResponse("<h2>Details for species: " + str(species_id) + "</h2>")
#
#
#
# # Create your views here.

