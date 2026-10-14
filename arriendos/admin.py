from django.contrib import admin

from .models import Arriendo, Equipo


class ArriendoInline(admin.TabularInline):
    model = Arriendo
    extra = 0


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "categoria",
        "marca",
        "modelo",
        "valor_diario",
        "disponible",
    )
    list_filter = ("categoria", "disponible")
    search_fields = ("nombre", "marca", "modelo")
    inlines = (ArriendoInline,)


@admin.register(Arriendo)
class ArriendoAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "equipo",
        "arrendatario",
        "fecha_inicio",
        "fecha_termino",
        "valor_total",
        "estado",
    )
    list_filter = ("estado", "fecha_inicio", "fecha_termino")
    search_fields = ("codigo", "arrendatario", "equipo__nombre")
