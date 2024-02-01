from django.contrib import admin
from .models import Record, Emailtemplate, Ausflugspaket, Subpaket
# Register your models here.

admin.site.register(Record)
admin.site.register(Emailtemplate)
admin.site.register(Ausflugspaket)
admin.site.register(Subpaket)

