from django.contrib import admin
from .models import *


class EserciziAdmin(admin.ModelAdmin):
    list_display = [
        "ExID",
        "category",
        "name",
        "description",
        "ripetizioni",
        "carico",
    ]


admin.site.register(Esercizi, EserciziAdmin)
admin.site.register(Scheda)
admin.site.register(SchedaAssign)
admin.site.register(UserAssign)
