from __future__ import unicode_literals

from django.db import models


class Sound(models.Model):
    name = models.CharField(max_length=20)
    abbreviation = models.CharField(max_length=5)

    def __str__(self):
        return self.name


class Rhythm(models.Model):
    name = models.CharField(max_length=20)

    @property
    def timing(self):
        return self.beatplays.all().count()

    def __str__(self):
        return self.name


class Polyrhythm(models.Model):
    poly_name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    rhythm1 = models.ForeignKey(Rhythm, related_name='rhythm1', default=None, null=True)
    rhythm2 = models.ForeignKey(Rhythm, related_name='rhythm2', default=None, null=True)

    def __str__(self):
        return self.poly_name


class Beatplay(models.Model):
    order = models.IntegerField()
    sounds = models.ManyToManyField(Sound)
    related_rhythm = models.ForeignKey(Rhythm, related_name='beatplays')

    def __str__(self):
        return self.order
