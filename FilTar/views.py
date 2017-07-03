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

def namedtuplefetchall(cursor):     #"Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def query_database(form_algorithm, form_species, experiment_ID, form_TPM, form_genes, form_Mirnas):

    cursor = connection.cursor()
    if bool(form_genes) == True and bool(form_Mirnas) == True:
        mirna_column = ""
        gene_column = ""
        mirna_filter = "AND c.mirna_id = %s "
        gene_filter = " AND r.Gene_Name = %s"
        param = [form_Mirnas, form_species, experiment_ID, form_TPM, form_genes]

    elif bool(form_genes) == False and bool(form_Mirnas) == True:
        mirna_column = ""
        gene_column = "r.Gene_Name, "
        mirna_filter = "AND c.mirna_id = %s "
        gene_filter = ""
        param = [form_Mirnas, form_species, experiment_ID, form_TPM]

    else:       # if gene form is selected but the mirna form isn't
        mirna_column = "c.mirna_id, "
        gene_column = ""
        mirna_filter = ""
        gene_filter = " AND r.Gene_Name = %s"
        param = [form_species, experiment_ID, form_TPM, form_genes]

    if form_algorithm == "contextpp":
        site_type = ", c.Site_Type"

    else:
        site_type = ""

    query = "SELECT '" + form_algorithm + "' as name, e.TPM, " + mirna_column + "c.mrna_id, " + gene_column + "c.score, c.UTR_START, c.UTR_END" + site_type +  " FROM " + form_algorithm
    query += " c JOIN expression_profiles e ON c.mrna_id = e.mrnas_id " + mirna_filter + "AND c.Species = %s AND e.experiments_id = %s AND e.TPM >= %s JOIN mRNAs r ON c.mrna_id = r.mRNA_ID"
    query += gene_filter

    cursor.execute(query, param)

    rows = namedtuplefetchall(cursor)
    return rows

def results(request):

    form_Mirnas = request.session.get('mirna')
    form_genes = request.session.get('gene')
    form_species = request.session.get('species')
    form_TPM = request.session.get('tpm')
    form_algorithm = request.session.get('algorithm')
    form_tissue = request.session.get('tissue')

    experiments = Experiments.objects.filter(species=form_species).filter(tissue=form_tissue).values()
    experiment_ID = experiments[0]['experiment_name']  # Change this

    if form_algorithm[0] == "contextpp":
        template = 'filtar/contextpptable'
    else:
        template = 'filtar/miRandatable'

    if form_genes != 'None' and form_Mirnas != 'None' and len(form_algorithm) == 1:

        template += "_mirna_gene.html"
        rows = query_database(form_algorithm[0], form_species, experiment_ID, form_TPM, form_Mirnas=form_Mirnas, form_genes=form_genes)
        return render(request, template, {'rows': rows, 'mirna': form_Mirnas, 'gene': form_genes, 'algorithm': form_algorithm[0]})

    elif form_genes != 'None' and form_Mirnas != 'None' and len(form_algorithm) != 1:
        row_one = query_database(form_algorithm[0], form_species, experiment_ID, form_TPM, form_Mirnas=form_Mirnas,
                                 form_genes=form_genes)
        row_two = query_database(form_algorithm[1], form_species, experiment_ID, form_TPM, form_Mirnas=form_Mirnas,
                                 form_genes=form_genes)
        rows = row_one + row_two
        return render(request, 'filtar/generic_table_mirna_gene.html', {'rows': rows, 'mirna': form_Mirnas, 'gene': form_genes})

    elif form_Mirnas != "None" and len(form_algorithm) == 1:   # Single algorithm

        template += ".html"
        rows = query_database(form_algorithm[0], form_species, experiment_ID, form_TPM, form_Mirnas=form_Mirnas, form_genes=False)
        return render(request, template, {'rows': rows, 'mirna': form_Mirnas, 'algorithm': form_algorithm[0]})

    elif form_Mirnas != "None" and len(form_algorithm) != 1:  # Multiple algorithms
        row_one = query_database(form_algorithm[0], form_species, experiment_ID, form_TPM, form_Mirnas=form_Mirnas,
                                 form_genes=False)
        row_two = query_database(form_algorithm[1], form_species, experiment_ID, form_TPM, form_Mirnas=form_Mirnas,
                                 form_genes=False)
        rows = row_one + row_two
        return render(request, 'filtar/generic_table.html', {'rows': rows, 'mirna': form_Mirnas, 'gene': form_genes})

    elif form_genes != "None" and len(form_algorithm) == 1:

        template += "_gene.html"
        rows = query_database(form_algorithm[0], form_species, experiment_ID, form_TPM, form_Mirnas=False, form_genes=form_genes)
        return render(request, template, {'rows': rows, 'gene': form_genes, 'algorithm': form_algorithm[0]})

    else:
        row_one = query_database(form_algorithm[0], form_species, experiment_ID, form_TPM, form_Mirnas=False,
                                 form_genes=form_genes)
        row_two = query_database(form_algorithm[1], form_species, experiment_ID, form_TPM, form_Mirnas=False,
                                 form_genes=form_genes)
        rows = row_one + row_two
        return render(request, 'filtar/generic_table_gene.html', {'rows': rows, 'mirna': form_Mirnas, 'gene': form_genes})


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