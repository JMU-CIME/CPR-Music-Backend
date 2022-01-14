from django.db import models

from teleband.instruments.models import Transposition


class EnsembleType(models.Model):

    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Ensemble Type"
        verbose_name_plural = "Ensemble Types"

    def __str__(self):
        return self.name


class Composer(models.Model):

    name = models.CharField(max_length=255)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Piece(models.Model):

    name = models.CharField(max_length=255)
    composer = models.ForeignKey(Composer, on_delete=models.PROTECT)
    video = models.URLField(blank=True)
    audio = models.URLField(blank=True)
    date_composed = models.DateField(null=True, blank=True)
    ensemble_type = models.ForeignKey(EnsembleType, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class PartType(models.Model):

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Part(models.Model):

    name = models.CharField(max_length=255)
    part_type = models.ForeignKey(PartType, on_delete=models.PROTECT)
    piece = models.ForeignKey(Piece, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class PartTransposition(models.Model):

    part = models.ForeignKey(Part, on_delete=models.PROTECT)
    transposition = models.ForeignKey(Transposition, on_delete=models.PROTECT)
    notation = models.URLField()

    class Meta:
        verbose_name = "Part Transposition"
        verbose_name_plural = "Part Transpositions"

    def __str__(self):
        return f"{self.part.piece}: {self.part} [{self.transposition}]"
