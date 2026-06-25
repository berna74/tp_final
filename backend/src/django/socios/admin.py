from django.contrib import admin

from .models import Socio


@admin.register(Socio)
class SocioAdmin(admin.ModelAdmin):
    list_display = ("id", "apellido", "nombre", "dni", "email", "registra_deuda")
    search_fields = ("apellido", "nombre", "dni", "email")
