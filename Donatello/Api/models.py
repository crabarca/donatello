from django.db import models

# Create your models here.

class Deputy(models.Model):
    nombre = models.CharField(max_length=100)
    comuna = models.CharField(max_length=100)
    distrito = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    partido = models.CharField(max_length=100)
    bancada = models.CharField(max_length=100)
    periodo = models.DateField(max_length=100)

class Operational(models.Model):
  diputado = models.ForeignKey(
    'Deputy',
    on_delete = models.CASCADE
  )

  # apoyo = models.IntegerField()
  # telefonia = models.IntegerField()
  # traslacion = models.IntegerField()
  # difusion = models.IntegerField()
  # interaccion = models.IntegerField()
  # arriendo = models.IntegerField()
  # consumos_basicos = models.IntegerField()
  # equipamiento = models.IntegerField()
  # art_oficina = models.IntegerField()
  # correspondencia = models.IntegerField()
  # mant_oficina = models.IntegerField()
  # repar_inmueble = models.IntegerField()
  # habil_sede = models.IntegerField()
  # seguro = models.IntegerField()
  # arriendo_ov = models.IntegerField()
  # web = models.IntegerField()
  # almacenamiento = models.IntegerField()
  # arriendo_om = models.IntegerField()
  # mant_om = models.IntegerField()
  # menores = models.IntegerField()

