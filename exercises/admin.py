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
        "isDefault",
    ]

class SchedaAdmin(admin.ModelAdmin):
    list_display = [
        "NomeScheda",
        "isDefault"
    ]

class SchedaAssignAdmin(admin.ModelAdmin):
    list_display = [
        "Esercizio",
        "Scheda",
        "IsDone",
    ]

class UserAssignAdmin(admin.ModelAdmin):
    list_display = [
        "User",
        "Scheda",
    ]

class ExUserAssignAdmin(admin.ModelAdmin):
    list_display = [
        "UserRef",
        "ExRef",
        "IsDone",
    ]

admin.site.register(Esercizi, EserciziAdmin)
admin.site.register(Scheda, SchedaAdmin)
admin.site.register(SchedaAssign, SchedaAssignAdmin)
admin.site.register(UserAssign, UserAssignAdmin)
admin.site.register(ExUserAssign, ExUserAssignAdmin)
