from django.contrib import admin

# Register your models here.

from operation.models import TypeOperation, FraisOperation, Operation

admin.site.register(TypeOperation)
admin.site.register(FraisOperation)
admin.site.register(Operation)
