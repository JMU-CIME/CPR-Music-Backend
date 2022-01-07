from django.db import models


class Transposition(models.Model):

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Instrument(models.Model):

    name = models.CharField(max_length=255)
    transposition = models.ForeignKey(Transposition, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
