from datetime import date
from decimal import Decimal

from django.contrib.auth.models import Group, Permission, User
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.test import TestCase

from .admin import ArriendoAdmin, EquipoAdmin
from .models import Arriendo, Equipo


class EquipoArriendoTests(TestCase):
    def setUp(self):
        self.equipo = Equipo.objects.create(
            nombre="Taladro percutor",
            categoria=Equipo.Categoria.HERRAMIENTAS,
            marca="Bosch",
            modelo="GBH 2-26",
            valor_diario=Decimal("12990"),
        )

    def test_equipo_and_arriendo_have_readable_names(self):
        arriendo = Arriendo.objects.create(
            codigo="ARR-TEST",
            equipo=self.equipo,
            arrendatario="Camila Rojas",
            fecha_inicio=date(2026, 10, 14),
            fecha_termino=date(2026, 10, 16),
            valor_total=Decimal("25980"),
            estado=Arriendo.Estado.EN_CURSO,
        )

        self.assertEqual(str(self.equipo), "Taladro percutor")
        self.assertEqual(str(arriendo), "ARR-TEST - Camila Rojas")

    def test_deleting_equipo_deletes_its_arriendos(self):
        arriendo = Arriendo.objects.create(
            codigo="ARR-CASCADE",
            equipo=self.equipo,
            arrendatario="Camila Rojas",
            fecha_inicio=date(2026, 10, 14),
            fecha_termino=date(2026, 10, 16),
            valor_total=Decimal("25980"),
            estado=Arriendo.Estado.EN_CURSO,
        )

        self.equipo.delete()

        self.assertFalse(Arriendo.objects.filter(pk=arriendo.pk).exists())


class AdminPermissionTests(TestCase):
    def setUp(self):
        self.equipo_type = ContentType.objects.get_for_model(Equipo)
        self.arriendo_type = ContentType.objects.get_for_model(Arriendo)
        self.vendedor = Group.objects.create(name="Vendedor")
        self.supervisor = Group.objects.create(name="Supervisor")

        for content_type in (self.equipo_type, self.arriendo_type):
            permissions = Permission.objects.filter(
                content_type=content_type,
                codename__in=(
                    "add_equipo",
                    "change_equipo",
                    "view_equipo",
                    "add_arriendo",
                    "change_arriendo",
                    "view_arriendo",
                ),
            )
            self.vendedor.permissions.add(*permissions)
            self.supervisor.permissions.add(
                *permissions.filter(codename__startswith="view_")
            )

    def test_vendedor_can_add_change_and_view_but_not_delete(self):
        user = User.objects.create_user(
            username="vendedor_test",
            password="test-password",
            is_staff=True,
        )
        user.groups.add(self.vendedor)

        self.assertTrue(user.has_perm("arriendos.add_equipo"))
        self.assertTrue(user.has_perm("arriendos.change_arriendo"))
        self.assertTrue(user.has_perm("arriendos.view_equipo"))
        self.assertFalse(user.has_perm("arriendos.delete_equipo"))
        self.assertFalse(user.has_perm("arriendos.delete_arriendo"))

    def test_supervisor_can_only_view(self):
        user = User.objects.create_user(
            username="supervisor_test",
            password="test-password",
            is_staff=True,
        )
        user.groups.add(self.supervisor)

        self.assertTrue(user.has_perm("arriendos.view_equipo"))
        self.assertTrue(user.has_perm("arriendos.view_arriendo"))
        self.assertFalse(user.has_perm("arriendos.add_equipo"))
        self.assertFalse(user.has_perm("arriendos.change_arriendo"))
        self.assertFalse(user.has_perm("arriendos.delete_equipo"))


class AdminDisplayTests(TestCase):
    def test_amounts_are_formatted_as_chilean_pesos(self):
        equipo = Equipo(
            nombre="Taladro",
            categoria=Equipo.Categoria.HERRAMIENTAS,
            marca="Bosch",
            modelo="GBH 2-26",
            valor_diario=Decimal("12990"),
        )
        arriendo = Arriendo(
            codigo="ARR-TEST",
            equipo=equipo,
            arrendatario="Camila Rojas",
            fecha_inicio=date(2026, 10, 14),
            fecha_termino=date(2026, 10, 16),
            valor_total=Decimal("104970"),
            estado=Arriendo.Estado.EN_CURSO,
        )

        self.assertEqual(
            EquipoAdmin(Equipo, admin.site).valor_diario_clp(equipo),
            "$12.990",
        )
        self.assertEqual(
            ArriendoAdmin(Arriendo, admin.site).valor_total_clp(arriendo),
            "$104.970",
        )


class SeedDataCommandTests(TestCase):
    def test_seed_command_creates_required_data_and_permissions(self):
        call_command("seed_data", verbosity=0)
        call_command("seed_data", verbosity=0)

        self.assertEqual(Equipo.objects.count(), 3)
        self.assertEqual(Arriendo.objects.count(), 6)
        self.assertEqual(User.objects.count(), 3)

        gerente = User.objects.get(username="gerente")
        vendedor = User.objects.get(username="vendedor")
        supervisor = User.objects.get(username="supervisor")
        self.assertTrue(gerente.is_superuser and gerente.is_staff)
        self.assertTrue(gerente.check_password("Inacap.2026"))
        self.assertEqual(
            list(vendedor.groups.values_list("name", flat=True)),
            ["Vendedor"],
        )
        self.assertTrue(vendedor.is_staff and not vendedor.is_superuser)
        self.assertTrue(vendedor.check_password("Inacap.2026"))
        self.assertTrue(vendedor.has_perm("arriendos.add_equipo"))
        self.assertTrue(vendedor.has_perm("arriendos.change_arriendo"))
        self.assertFalse(vendedor.has_perm("arriendos.delete_equipo"))
        self.assertEqual(
            list(supervisor.groups.values_list("name", flat=True)),
            ["Supervisor"],
        )
        self.assertTrue(supervisor.is_staff and not supervisor.is_superuser)
        self.assertTrue(supervisor.check_password("Inacap.2026"))
        self.assertTrue(supervisor.has_perm("arriendos.view_arriendo"))
        self.assertFalse(supervisor.has_perm("arriendos.add_equipo"))
        self.assertFalse(supervisor.has_perm("arriendos.change_equipo"))
        self.assertFalse(supervisor.has_perm("arriendos.delete_arriendo"))
