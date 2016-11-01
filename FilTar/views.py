# from django.http import Http404
from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from FilTar.models import Species

def index(request):
	 all_species = Species.objects.all() 
	 #template = loader.get_template('FilTar/index.html')
	 context = {	'all_species' : all_species, }
	 return render(request, 'filtar/index.html', context)
# 	html = ()
# 	for species in all_species:
# 	     url = '/filtar/' + str(species.id) + '/'
# 	     html += ('<a href="' + url + '">' + species.common_name + '</a><br>',)
	

def detail(request, species_id):
# 	try:
# 		species = Species.objects.get(pk=species_id)
# 	except Species.DoesNotExist:
# 		raise Http404("Species does not exist")
	species = get_object_or_404(Species, pk=species_id)
	return render(request, 'filtar/detail.html', ({'species': species}) )
# 	return HttpResponse("<h2>Details for Species id: " + str(species_id) + "</h2>")



# 	return HttpResponse("<h2>Details for species: " + str(species_id) + "</h2>")



# Create your views here.

