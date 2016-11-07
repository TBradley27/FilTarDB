from django.views import generic
# from django.views.generic.edit import CreateView
from .models import Species
from .models import Mirnas
from .models import MirnaForm
from .models import Contextpp
from .models import Contextpp_Form
from .forms import TPMForm
from .forms import MirnaForm
from .forms import TissueForm
from .forms import SpeciesForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.forms import ModelChoiceField

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
        if form_Mirnas.is_valid() and form_species.is_valid():
             form_species = form_species.cleaned_data['Species']
             form_Mirnas = form_Mirnas.cleaned_data['mirnas']
             scores = Contextpp.objects.filter(mirna_name=form_Mirnas
                                               ).filter(
                 common_name=form_species)

        return render(request, 'filtar/contextpptable.html', {'scores': scores} )

    else:
        form_TPM = TPMForm()
        form_Mirnas = MirnaForm()
        # form_tissue = TissueForm()
        form_species = SpeciesForm()

    return render(request, 'filtar/testing.html',{'form_Mirnas': form_Mirnas, 'form_species': form_species, 'form_TPM': form_TPM})


                                                  #
                                                  # 'form_tissue': form_tissue, })

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

