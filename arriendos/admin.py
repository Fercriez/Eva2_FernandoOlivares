from django.contrib import admin

from .models import Arriendo, Equipo


class ArriendoInline(admin.TabularInline):
    model = Arriendo
    extra = 0


def _format_clp(value):
    return f"${value:,.0f}".replace(",", ".")


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "categoria",
        "marca",
        "modelo",
        "valor_diario_clp",
        "disponible",
    )
    list_filter = ("categoria", "disponible")
    search_fields = ("nombre", "marca", "modelo")
    inlines = (ArriendoInline,)

    @admin.display(description="Valor diario", ordering="valor_diario")
    def valor_diario_clp(self, obj):
        return _format_clp(obj.valor_diario)


@admin.register(Arriendo)
class ArriendoAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "equipo",
        "arrendatario",
        "fecha_inicio",
        "fecha_termino",
        "valor_total_clp",
        "estado",
    )
    list_filter = ("estado", "fecha_inicio", "fecha_termino")
    search_fields = ("codigo", "arrendatario", "equipo__nombre")

    @admin.display(description="Valor total", ordering="valor_total")
    def valor_total_clp(self, obj):
        return _format_clp(obj.valor_total)
