from django.contrib import admin
from .models import Species
from .models import Tissues
from .models import Mrnas
from .models import Mirnas
from .models import TModel

admin.site.register(Species)
admin.site.register(Tissues)
admin.site.register(Mrnas)
admin.site.register(Mirnas)
admin.site.register(TModel)


# Register your models here.
