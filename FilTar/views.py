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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from operator import itemgetter
from django.http import HttpResponse
import csv
from django.http import StreamingHttpResponse

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def results(request):

    form_Mirnas = request.session.get('mirna')


    form_species = request.session.get('species')
    form_TPM = request.session.get('tpm')
    form_algorithm = request.session.get('algorithm')
    form_tissue = request.session.get('tissue')

    experiments = Experiments.objects.filter(species=form_species).filter(tissue=form_tissue).values()
    experiment_ID = experiments[0]['experiment_name']  # Change this

    if form_algorithm == 'TargetScan7':

        cursor = connection.cursor()
        cursor.execute('''
                                      SELECT e.TPM, c.mrna_id, r.Gene_Name, c.contextpp_score, c.UTR_START, c.UTR_END, c.Site_Type
                                      FROM contextpp c
                                      JOIN expression_profiles e
                                      ON c.mrna_id = e.mrnas_id
                                      AND c.mirna_id = %s
                                      AND c.Species = %s
                                      AND e.experiments_id = %s
                                      AND e.TPM >= %s
                                      JOIN mRNAs r ON c.mrna_id = r.mRNA_ID''',
                       [form_Mirnas, form_species, experiment_ID, form_TPM])

        rows = namedtuplefetchall(cursor)

        page = request.GET.get('page')

        # paginator = Paginator(row, 30)
        # try:
        #     rows = paginator.page(page)
        # except PageNotAnInteger:
        #     rows = paginator.page(1)
        # except EmptyPage:
        #     rows = paginator.page(paginator.num_pages)
        #
        # if request.GET.get('format') is not None:
        #     if request.GET['format'] == 'csv':
        #         response = HttpResponse('')
        #         response['Content-Disposition'] = 'attachment; filename={}.csv'.format(form_Mirnas)
        #         writer = csv.writer(response, dialect=csv.excel)
        #         # writer.writerow(['a','b'])
        #         response = StreamingHttpResponse((writer.writerow(row) for row in rows),
        #                                          content_type="text/csv")
        #         return response

        return render(request, 'filtar/contextpptable.html', {'rows': rows, 'mirna': form_Mirnas})

def home(request):

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

             request.session['species'] = form_species
             request.session['mirna'] = str(form_Mirnas)
             request.session['tpm'] = form_TPM
             request.session['tissue'] = str(form_tissue)
             request.session['algorithm'] = form_algorithm

             return HttpResponseRedirect('/filtar/results')



             # elif form_algorithm == 'miRanda':
             #
             #     # scores = MiRanda.objects.filter(mirna=form_Mirnas
             #     #                                   ).filter(
             #     #     species=form_species)
             #
             #     cursor = connection.cursor()
             #     cursor.execute('''SELECT e.TPM, m.Mrnas, m.Mirnas, m.miRanda_score, m.UTR_start, m.UTR_end
             #                                       FROM miRanda m
             #                                       JOIN expression_profiles e
             #                                       ON m.Mrnas = e.mrnas_id
             #                                       AND m.Mirnas = %s
             #                                       AND m.Species = %s
             #                                       AND e.experiments_id = %s
             #                                       AND e.TPM >= %s''', [form_Mirnas, form_species, experiment_ID, form_TPM])
             #     row = namedtuplefetchall(cursor)
             #
             #     tpm = []
             #     Mirnas = []
             #     utr_start = []
             #     utr_end = []
             #     Mrnas = []
             #     miranda_score = []
             #
             #     for x in range(0, len(row)):
             #         tpm.append(str(row[x].TPM))
             #         Mirnas.append((row[x].Mirnas))
             #         Mrnas.append((row[x].Mrnas))
             #         utr_start.append((row[x].UTR_start))
             #         utr_end.append((row[x].UTR_end))
             #         miranda_score.append((row[x].miRanda_score))
             #
             #     x = zip(Mirnas, Mrnas, miranda_score, tpm, utr_start, utr_end)
             #
             #     return render(request, 'filtar/miRandatable.html', {'x': x})
             #
             #
             # else:
             #
             #     scores = PITA.objects.filter(mirna=form_Mirnas
             #                                     ).filter(
             #         species=form_species)
             #
             #     cursor = connection.cursor()
             #     cursor.execute('''SELECT e.TPM, p.Mrnas, p.Mirnas, p.PITA_score, p.UTR_START, p.UTR_END
             #                                                        FROM PITA p
             #                                                        JOIN expression_profiles e
             #                                                        ON p.Mrnas = e.mrnas_id
             #                                                        AND p.Mirnas = %s
             #                                                        AND p.Species = %s
             #                                                        AND e.experiments_id = %s
             #                                                        AND e.TPM >= %s''',
             #                    [form_Mirnas, form_species, experiment_ID, form_TPM])
             #     row = namedtuplefetchall(cursor)
             #
             #     tpm = []
             #     Mirnas= []
             #     Mrnas = []
             #     PITA_score = []
             #     start = []
             #     end = []
             #     for x in range(0, len(row)):
             #         tpm.append(str(row[x].TPM))
             #         Mirnas.append((row[x].Mirnas))
             #         Mrnas.append((row[x].Mrnas))
             #         PITA_score.append((row[x].PITA_score))
             #         start.append((row[x].UTR_START))
             #         end.append((row[x].UTR_END))
             #
             #     x = zip(Mirnas, Mrnas, start, end, PITA_score, tpm)
             #
             #     return render(request, 'filtar/pitatable.html', {'scores': scores, 'x': x})

    elif request.method == 'GET':
        form_TPM = TPMForm()
        form_Mirnas = MirnaForm()
        form_tissue = TissueForm()
        form_species = SpeciesForm()
        form_algorithm = AlgorithmForm()

    return render(request, 'filtar/testing.html',{'form_Mirnas': form_Mirnas, 'form_species': form_species, 'form_TPM': form_TPM,
                                                  'form_algorithm': form_algorithm, 'form_tissue': form_tissue,  })
