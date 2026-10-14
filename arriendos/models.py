from django.db import models


class Equipo(models.Model):
    class Categoria(models.TextChoices):
        HERRAMIENTAS = "herramientas", "Herramientas"
        AUDIOVISUAL = "audiovisual", "Audiovisual"
        CONSTRUCCION = "construccion", "Construcción"

    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=Categoria.choices)
    marca = models.CharField(max_length=60)
    modelo = models.CharField(max_length=60)
    valor_diario = models.DecimalField(max_digits=10, decimal_places=0)
    disponible = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "equipo"
        verbose_name_plural = "equipos"

    def __str__(self):
        return self.nombre


class Arriendo(models.Model):
    class Estado(models.TextChoices):
        RESERVADO = "reservado", "Reservado"
        EN_CURSO = "en_curso", "En curso"
        FINALIZADO = "finalizado", "Finalizado"

    codigo = models.CharField(max_length=20, unique=True)
    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        related_name="arriendos",
    )
    arrendatario = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=0)
    estado = models.CharField(max_length=20, choices=Estado.choices)

    class Meta:
        ordering = ["-fecha_inicio", "codigo"]
        verbose_name = "arriendo"
        verbose_name_plural = "arriendos"

    def __str__(self):
        return f"{self.codigo} - {self.arrendatario}"
