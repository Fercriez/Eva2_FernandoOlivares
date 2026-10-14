from datetime import date
from decimal import Decimal

from django.contrib.auth.models import Group, Permission, User
from django.core.management.base import BaseCommand

from arriendos.models import Arriendo, Equipo


class Command(BaseCommand):
    help = "Carga equipos, arriendos, grupos y usuarios de demostración."

    def handle(self, *args, **options):
        equipos = [
            {
                "nombre": "Taladro percutor",
                "categoria": Equipo.Categoria.HERRAMIENTAS,
                "marca": "Bosch",
                "modelo": "GBH 2-26",
                "valor_diario": Decimal("12990"),
                "disponible": True,
            },
            {
                "nombre": "Generador eléctrico",
                "categoria": Equipo.Categoria.CONSTRUCCION,
                "marca": "Honda",
                "modelo": "EU22i",
                "valor_diario": Decimal("34990"),
                "disponible": True,
            },
            {
                "nombre": "Proyector portátil",
                "categoria": Equipo.Categoria.AUDIOVISUAL,
                "marca": "Epson",
                "modelo": "PowerLite X49",
                "valor_diario": Decimal("24990"),
                "disponible": False,
            },
        ]
        equipos_por_nombre = {}
        for datos in equipos:
            equipo, _ = Equipo.objects.update_or_create(
                nombre=datos["nombre"],
                defaults=datos,
            )
            equipos_por_nombre[equipo.nombre] = equipo

        arriendos = [
            {
                "codigo": "ARR-2026-001",
                "equipo": equipos_por_nombre["Taladro percutor"],
                "arrendatario": "Camila Rojas",
                "fecha_inicio": date(2026, 10, 12),
                "fecha_termino": date(2026, 10, 14),
                "valor_total": Decimal("25980"),
                "estado": Arriendo.Estado.EN_CURSO,
            },
            {
                "codigo": "ARR-2026-002",
                "equipo": equipos_por_nombre["Generador eléctrico"],
                "arrendatario": "Constructora Los Andes",
                "fecha_inicio": date(2026, 10, 13),
                "fecha_termino": date(2026, 10, 16),
                "valor_total": Decimal("104970"),
                "estado": Arriendo.Estado.EN_CURSO,
            },
            {
                "codigo": "ARR-2026-003",
                "equipo": equipos_por_nombre["Proyector portátil"],
                "arrendatario": "Diego Muñoz",
                "fecha_inicio": date(2026, 10, 15),
                "fecha_termino": date(2026, 10, 16),
                "valor_total": Decimal("49980"),
                "estado": Arriendo.Estado.RESERVADO,
            },
            {
                "codigo": "ARR-2026-004",
                "equipo": equipos_por_nombre["Taladro percutor"],
                "arrendatario": "Servicios del Sur",
                "fecha_inicio": date(2026, 10, 8),
                "fecha_termino": date(2026, 10, 10),
                "valor_total": Decimal("25980"),
                "estado": Arriendo.Estado.FINALIZADO,
            },
            {
                "codigo": "ARR-2026-005",
                "equipo": equipos_por_nombre["Generador eléctrico"],
                "arrendatario": "Paula Fernández",
                "fecha_inicio": date(2026, 10, 17),
                "fecha_termino": date(2026, 10, 18),
                "valor_total": Decimal("69980"),
                "estado": Arriendo.Estado.RESERVADO,
            },
            {
                "codigo": "ARR-2026-006",
                "equipo": equipos_por_nombre["Proyector portátil"],
                "arrendatario": "Instituto Central",
                "fecha_inicio": date(2026, 10, 6),
                "fecha_termino": date(2026, 10, 7),
                "valor_total": Decimal("49980"),
                "estado": Arriendo.Estado.FINALIZADO,
            },
        ]
        for datos in arriendos:
            Arriendo.objects.update_or_create(
                codigo=datos["codigo"],
                defaults=datos,
            )

        permisos = Permission.objects.filter(
            content_type__app_label="arriendos",
            codename__in=[
                f"{accion}_{modelo}"
                for modelo in ("equipo", "arriendo")
                for accion in ("add", "change", "view")
            ],
        )
        vendedor_group, _ = Group.objects.get_or_create(name="Vendedor")
        vendedor_group.permissions.set(permisos)

        supervisor_group, _ = Group.objects.get_or_create(name="Supervisor")
        supervisor_group.permissions.set(
            permisos.filter(codename__startswith="view_")
        )

        self._configure_user(
            username="gerente",
            email="gerente@example.com",
            password="Inacap.2026",
            is_superuser=True,
            groups=[],
        )
        self._configure_user(
            username="vendedor",
            email="vendedor@example.com",
            password="Inacap.2026",
            is_superuser=False,
            groups=[vendedor_group],
        )
        self._configure_user(
            username="supervisor",
            email="supervisor@example.com",
            password="Inacap.2026",
            is_superuser=False,
            groups=[supervisor_group],
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Datos cargados: 3 equipos, 6 arriendos y 3 usuarios."
            )
        )

    @staticmethod
    def _configure_user(username, email, password, is_superuser, groups):
        user, _ = User.objects.get_or_create(username=username)
        user.email = email
        user.is_staff = True
        user.is_superuser = is_superuser
        user.is_active = True
        user.set_password(password)
        user.save()
        user.groups.set(groups)
