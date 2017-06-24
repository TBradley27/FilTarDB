from django.views import generic
from .models import *
from .forms import *
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import ModelChoiceField
from itertools import chain
from django.db import connection
from collections import namedtuple
import decimal
from operator import itemgetter

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def results(request):

    form_Mirnas = request.session.get('mirna')
    form_genes = request.session.get('gene')
    form_species = request.session.get('species')
    form_TPM = request.session.get('tpm')
    form_algorithm = request.session.get('algorithm')
    form_tissue = request.session.get('tissue')

    experiments = Experiments.objects.filter(species=form_species).filter(tissue=form_tissue).values()
    experiment_ID = experiments[0]['experiment_name']  # Change this

    if form_algorithm == 'TargetScan7':

        # random

        if form_genes != 'None' and form_Mirnas != 'None':

            # User selects miRNA and gene

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
                                          JOIN mRNAs r ON c.mrna_id = r.mRNA_ID
                                          AND r.Gene_Name = %s''',
                           [form_Mirnas, form_species, experiment_ID, form_TPM, form_genes])

        elif form_Mirnas != "None":

            # Users selects the miRNA only

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

        else:

            # User selects the gene only

            cursor = connection.cursor()
            cursor.execute('''
                                          SELECT e.TPM, c.mirna_id, c.mrna_id, c.contextpp_score, c.UTR_START, c.UTR_END, c.Site_Type
                                          FROM contextpp c
                                          JOIN expression_profiles e
                                          ON c.mrna_id = e.mrnas_id
                                          AND c.Species = %s
                                          AND e.experiments_id = %s
                                          AND e.TPM >= %s
                                          JOIN mRNAs r ON c.mrna_id = r.mRNA_ID
                                          AND r.Gene_Name = %s''',
                           [form_species, experiment_ID, form_TPM, form_genes])

            rows = namedtuplefetchall(cursor)
            return render(request, 'filtar/contextpptable_gene.html', {'rows': rows, 'gene': form_genes})

        rows = namedtuplefetchall(cursor)

        return render(request, 'filtar/contextpptable.html', {'rows': rows, 'mirna': form_Mirnas})

def home(request):

    if request.method == 'POST':
        form_Mirnas = MirnaForm(request.POST)
        form_genes = GeneForm(request.POST)
        form_species = SpeciesForm(request.POST)
        form_TPM = TPMForm(request.POST)
        form_tissue = TissueForm(request.POST)
        form_algorithm = AlgorithmForm(request.POST)

        if form_Mirnas.is_valid() and form_species.is_valid() and form_TPM.is_valid() and form_tissue.is_valid() and form_algorithm.is_valid() and form_genes.is_valid():
             form_species = form_species.cleaned_data['Species']
             form_Mirnas = form_Mirnas.cleaned_data['mirna']
             form_genes = form_genes.cleaned_data['gene']
             form_TPM =  form_TPM.cleaned_data['TPM_threshold']
             form_tissue = form_tissue.cleaned_data['Tissue']
             form_algorithm = form_algorithm.cleaned_data['Algorithm']

             request.session['species'] = form_species
             request.session['mirna'] = str(form_Mirnas)
             request.session['gene'] = str(form_genes)
             request.session['tpm'] = form_TPM
             request.session['tissue'] = str(form_tissue)
             request.session['algorithm'] = form_algorithm

             return HttpResponseRedirect('/filtar/results')

    elif request.method == 'GET':
        form_TPM = TPMForm()
        form_Mirnas = MirnaForm()
        form_genes = GeneForm()
        form_tissue = TissueForm()
        form_species = SpeciesForm()
        form_algorithm = AlgorithmForm()

    return render(request, 'filtar/home.html',{'form_Mirnas': form_Mirnas, 'form_species': form_species, 'form_TPM': form_TPM,
                                                  'form_algorithm': form_algorithm, 'form_tissue': form_tissue, 'form_genes': form_genes  })








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