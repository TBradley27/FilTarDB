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

try:
    from django.urls import reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse_lazy


mean = {'contextpp': decimal.Decimal(-0.0578464) ,'miRanda': decimal.Decimal(147.081730)}
sd = {'contextpp': decimal.Decimal(-0.275078),'miRanda': decimal.Decimal(6.672571)} #Sign reflects whether more positive score is a good or bad thing
# the sample standard deviation is used here - though pop and sample sd is virtually identical

def namedtuplefetchall(cursor):     # Create a list of named tuples - 1 row of query results = 1 named tuple
    desc = cursor.description       
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def get_normalised_scores(rows, mean_score,sd):
    norm_scores = []
    for row in rows:
        distance = row.score - mean_score  #Absolute value accounta for -ve sign of the TargetScan score
        z_score = distance / sd
        norm_scores.append('{0:.2f}'.format(z_score))
    merged_results = zip(rows, norm_scores)
    return merged_results

def map_avg_tpms(results_list, list_of_transcripts, list_of_TPMs):
    dummy_list = []
    for i in range(0, len(results_list)):
        for j in range(0, len(list_of_transcripts)):
            if results_list[i] == list_of_transcripts[j]:
                dummy_list.append(list_of_TPMs[j])
            else:
                pass

    return dummy_list

def query_database(form_algorithm, form_species, form_tissue, form_TPM, form_genes, form_Mirnas):

    if bool(form_genes) == True and bool(form_Mirnas) == True:
        mirna_column = ""
        gene_column = ""
        mirna_filter = "AND c.mirna_id = %s "
        gene_filter = " AND r.Gene_ID = %s"
        param = [form_Mirnas, form_species, form_tissue, form_TPM, form_genes]

    elif bool(form_genes) == False and bool(form_Mirnas) == True:
        mirna_column = ""
        gene_column = "r.Gene_ID, "
        mirna_filter = "AND c.mirna_id = %s "
        gene_filter = ""
        param = [form_Mirnas, form_species, form_tissue, form_TPM] # the sample ID refers to the experiment ID

    else:       # if gene form is selected but the mirna form isn't
        mirna_column = "c.mirna_id, "
        gene_column = ""
        mirna_filter = ""
        gene_filter = " AND r.Gene_ID = %s"
        param = [form_species, form_tissue, form_TPM, form_genes]

    if form_algorithm == "contextpp":
        algorithm_name = "TargetScan7"
        site_type = ", c.Site_Type"

    elif form_algorithm == "miRanda":
        site_type = ""
        algorithm_name = "miRanda"

    else:
        site_type = ""
        algorithm_name = "PITA"

    query = "SELECT '" + algorithm_name + "' as name, e.TPM, " + mirna_column + "c.mrna_id, " + gene_column \
            + "c.score, c.UTR_START, c.UTR_END" + site_type + " FROM " + form_algorithm + \
            " c JOIN expression_profiles e ON c.mrna_id = e.mrnas_id " + mirna_filter\
            + "AND c.Species = %s AND e.experiments_id = %s AND e.TPM >= %s JOIN mRNA r ON c.mrna_id = r.mRNA_ID" + \
            gene_filter

    cursor = connection.cursor()
    cursor.execute(query, param)

    rows = namedtuplefetchall(cursor)
    return rows

def query_genes(form_genes):
    cursor = connection.cursor()
    query = "SELECT m.mRNA_ID FROM mRNA m WHERE Gene_Name = %s"
    cursor.execute(query, [form_genes])
    rows = namedtuplefetchall(cursor)

    return rows

def query_expression(transcripts, form_tissue):
    cursor = connection.cursor()
    tx_list = []
    tpm_list= []
    tpm_mean = []
    for tx in range(0, len(transcripts)):
        tx_list.append(transcripts[tx]) # Index for labelled tuple element 'mRNA_ID'
        query = "SELECT TPM FROM expression_profiles WHERE mrnas_id IN %s AND experiments_id = %s" #For some reason the AVG function does not work here
        cursor.execute(query, [tx_list, form_tissue])
        rows = namedtuplefetchall(cursor)
        for i in range(0, len(rows)):
            tpm_list.append(rows[i][0])
        tpm_mean.append ( "%.3f" % ( sum(tpm_list) / len(tpm_list) ) )

    return tpm_mean

def results(request):
    form_Mirnas = request.session.get('mirna')
    form_genes = request.session.get('gene')
    form_species = request.session.get('species')
    form_TPM = request.session.get('tpm')
    form_algorithm = request.session.get('algorithm')
    form_tissue = request.session.get('tissues')

    samples = Samples.objects.filter(species=form_species).filter(tissue=form_tissue).values()

    sample_ID = [] # Initialise list
    run_ID = []

    for i in range(0, len(samples) ):
        sample_ID.append ( samples[i]['name'] )  # Get the first experiment_name returned from many
        runs = Runs.objects.filter(sample=samples[i]['name']).values()
        for j in range(0, len(runs) ):
              run_ID.append (runs[j]['name'])

    if form_algorithm[0] == "contextpp":
        template = 'filtardb/contextpptable'
    elif form_algorithm[0] == "miRanda":
        template = 'filtardb/miRandatable'

    if form_genes != 'None' and form_Mirnas != 'None' and len(form_algorithm) == 1:

        template += "_mirna_gene.html"
        rows = query_database(form_algorithm[0], form_species, form_tissue, form_TPM,
                              form_Mirnas=form_Mirnas, form_genes=form_genes)

        return render(request, template, {'rows': rows, 'mirna': form_Mirnas, 'gene': form_genes,
                                          'algorithm': form_algorithm[0], 'num_replicates': len(sample_ID),
                                          'replicates': sample_ID, 'sample': form_tissue, 'species': form_species})

    elif form_genes != 'None' and form_Mirnas != 'None' and len(form_algorithm) != 1:
        row_one = query_database(form_algorithm[0], form_species, form_tissue, form_TPM, form_Mirnas=form_Mirnas,
                                 form_genes=form_genes)
        row_one = get_normalised_scores(row_one, mean[form_algorithm[0]], sd[form_algorithm[0]])    #TargetScan7
        row_two = query_database(form_algorithm[1], form_species, form_tissue, form_TPM, form_Mirnas=form_Mirnas,
                                 form_genes=form_genes)
        row_two = get_normalised_scores(row_two, mean[form_algorithm[1]], sd[form_algorithm[1]])

        rows = list(row_one) + list(row_two)

        return render(request, 'filtardb/generic_table_mirna_gene.html', {'rows': rows, 'mirna': form_Mirnas,
                                                                        'gene': form_genes,'num_replicates': len(sample_ID),
                                                                        'replicates': sample_ID,'sample': form_tissue, 'species':form_species})

    elif form_Mirnas != "None" and len(form_algorithm) == 1:   # Single algorithm - miRNA

        template += ".html"
        rows = query_database(form_algorithm[0], form_species, form_tissue, form_TPM, form_Mirnas=form_Mirnas,
                              form_genes=False)
        result_transcripts = []        # This is specific to whether gene or form is selected
        for result in rows:
            result_transcripts.append(result[2])
        
        return render(request, template, {'rows': rows, 'mirna': form_Mirnas, 'algorithm': form_algorithm[0],
                                          'num_replicates': len(sample_ID),'replicates': sample_ID,
                                          'sample': form_tissue, 'species': form_species})

    elif form_Mirnas != "None" and len(form_algorithm) != 1:  # Multiple algorithms

        row_one = query_database(form_algorithm[0], form_species, form_tissue, form_TPM, form_Mirnas=form_Mirnas,
                                 form_genes=False)
        row_one = get_normalised_scores(row_one, mean[form_algorithm[0]], sd[form_algorithm[0]])

        row_two = query_database(form_algorithm[1], form_species, form_tissue, form_TPM, form_Mirnas=form_Mirnas,
                                 form_genes=False)
        row_two = get_normalised_scores(row_two, mean[form_algorithm[1]], sd[form_algorithm[1]])

        rows = list(row_one) + list(row_two)

        return render(request, 'filtardb/generic_table.html', {'rows': rows, 'mirna': form_Mirnas, 'gene': form_genes,
                                                             'num_replicates': len(sample_ID),
                                                             'replicates': sample_ID, 'sample': form_tissue, 'species': form_species})

    elif form_genes != "None" and len(form_algorithm) == 1:  # Just genes, one algorithm
        template += "_gene.html"
        rows = query_database(form_algorithm[0], form_species, form_tissue, form_TPM, form_Mirnas=False,
                              form_genes=form_genes)

        new_rows = []

        for result in rows:
              x = Utr_length.objects.filter(tissue_id=form_tissue).filter(mrna_id=result.mrna_id).values()
              utr_length = x[0]['utr_length']
              z = type(result)
              if utr_length > result[6]:
                   new_rows.append(result)
              else:
                   pass

        return render(request, template, {'rows': new_rows, 'gene': form_genes, 'num_replicates': len(sample_ID),
                                          'replicates' : sample_ID, 'runs' : run_ID,  'sample': form_tissue, 'species': form_species})

    elif form_genes != "None" and len(form_algorithm) != 1:
        row_one = query_database(form_algorithm[0], form_species, form_tissue, form_TPM, form_Mirnas=False,
                                 form_genes=form_genes)
        row_one = get_normalised_scores(row_one, mean[form_algorithm[0]], sd[form_algorithm[0]])

        row_two = query_database(form_algorithm[1], form_species, form_tissue, form_TPM, form_Mirnas=False,
                                 form_genes=form_genes)
        row_two = get_normalised_scores(row_two, mean[form_algorithm[1]], sd[form_algorithm[1]])

        rows = list(row_one) + list(row_two)

        return render(request, 'filtardb/generic_table_gene.html', {'rows': rows, 'mirna': form_Mirnas,
                                                                  'gene': form_genes, 'num_replicates': len(sample_ID),
                                                                  'replicates' : sample_ID, 'sample': form_tissue, 'species': form_species})

def get_avg_tpms(result_transcripts, form_tissue, rows):

    transcripts = set(result_transcripts)  # Removes duplicate entries
    transcripts = list(transcripts)  # Because set objects cannot be easily indexed

    tpm_means = query_expression(transcripts, form_tissue)

    avg_tpms = map_avg_tpms(result_transcripts, transcripts, tpm_means)
    rows = zip(rows, avg_tpms)
    rows = list(rows)

    return rows

def home(request):

    if request.method == 'POST':

        form_TPM = TPMForm(request.POST)
        form_algorithm = AlgorithmForm(request.POST)
        form_auto = ExampleFKForm(request.POST)

        if form_auto.is_valid() and form_algorithm.is_valid() and form_TPM.is_valid():

             form_TPM =  form_TPM.cleaned_data['TPM_threshold']
             form_algorithm = form_algorithm.cleaned_data['Algorithm']

             form_mirna = form_auto.cleaned_data['test']
             form_tissues = form_auto.cleaned_data['tissues']
             form_gene = form_auto.cleaned_data['gene']
             form_species = form_auto.cleaned_data['continent']

             request.session['gene'] = str(form_gene)
             request.session['tpm'] = str(form_TPM)
             request.session['algorithm'] = form_algorithm
             request.session['species'] = str(form_species)
             request.session['mirna'] = str(form_mirna)
             request.session['tissues'] = str(form_tissues)

             return HttpResponseRedirect('/results/')

    elif request.method == 'GET':

        form_auto = ExampleFKForm()
        form_TPM = TPMForm()
        form_algorithm = AlgorithmForm()

    return render(request, 'filtardb/home.html',{'form_auto': form_auto,
                                               'form_algorithm': form_algorithm,
                                               'form_TPM': form_TPM} )


class CountryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):


        qs = ExampleFK.objects.all()

        continent = self.forwarded.get('continent', None)

        if continent:
            qs = qs.filter(species=continent)

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return (qs)

class TissuesAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Tissues.objects.all()


        continent = self.forwarded.get('continent', None)

        if continent:
            qs = qs.filter(taxonomic_ID=continent)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return (qs)

class GeneAutocomplete(autocomplete.Select2QuerySetView):  #Controls form information displayed to the user
    def get_queryset(self):

        qs = Gene.objects.all()

        print(qs)

        continent = self.forwarded.get('continent', None)

        if continent:
            qs = Gene.objects.filter(gene_species__species_id=continent)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        print(qs)

        return (qs)

