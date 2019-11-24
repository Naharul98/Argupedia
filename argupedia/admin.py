from django.contrib import admin
from .models import Entry
from .models import Scheme
from.models import SchemeStructure
# Register your models here.
admin.site.register(Entry)
admin.site.register(Scheme)
admin.site.register(SchemeStructure)