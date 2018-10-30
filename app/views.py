# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from app.models import Polyrhythm, Rhythm, Beatplay, Sound
from app.forms import PolyrhythmForm, RhythmForm, Rhythm1BeatplayFormSet, Rhythm2BeatplayFormSet


class PolyrhythmList(View):
    def get(self, request):
        polys = Polyrhythm.objects.all()
        return render(request, 'polyrhythm_list.html', {'polys': polys})


class PolyrhythmEdit(View):
    def get(self, request, poly_id=None):
        poly = None
        rhythm1 = None
        rhythm2 = None
        if poly_id:
            poly = Polyrhythm.objects.get(id=poly_id)
            rhythm1 = poly.rhythm1
            rhythm2 = poly.rhythm2

        poly_form = PolyrhythmForm(instance=poly)
        rhythm1_form = RhythmForm(instance=rhythm1)
        rhythm1_beats_formset = Rhythm1BeatplayFormSet(instance=rhythm1, prefix='r1_formset')
        rhythm2_form = RhythmForm(instance=rhythm2)
        rhythm2_beats_formset = Rhythm2BeatplayFormSet(instance=rhythm2, prefix='r2_formset')
        return render(request, 'polyrhythm_form.html', {'poly_form': poly_form,
                                                        'rhythm1_form': rhythm1_form,
                                                        'rhythm1_beats_formset': rhythm1_beats_formset,
                                                        'rhythm2_form': rhythm2_form,
                                                        'rhythm2_beats_formset': rhythm2_beats_formset,
                                                        })


    def post(self, request, poly_id=None):
        poly = None
        rhythm1 = None
        rhythm2 = None
        if poly_id:
            poly = Polyrhythm.objects.get(id=poly_id)
            rhythm1 = poly.rhythm1
            rhythm2 = poly.rhythm2

        rhythm1_form = RhythmForm(request.POST, instance=rhythm1)
        rhythm2_form = RhythmForm(request.POST, instance=rhythm2)
        poly_form = PolyrhythmForm(request.POST, instance=poly)

        # CHECK IF ALL THINGS ARE VALID. IF SO, THEN...

        # RHYTHM 1 SAVING
        saved_rhythm1_form = rhythm1_form.save(commit=False)
        rhythm1_beats_formset = Rhythm1BeatplayFormSet(request.POST, instance=saved_rhythm1_form, prefix='r1_formset')
        if rhythm1_beats_formset.is_valid():
            saved_rhythm1_form.save()
            rhythm1_beats_formset.save()

        # RHYTHM 2 SAVING
        saved_rhythm2_form = rhythm2_form.save(commit=False)
        rhythm2_beats_formset = Rhythm2BeatplayFormSet(request.POST, instance=saved_rhythm2_form, prefix='r2_formset')
        if rhythm2_beats_formset.is_valid():
            saved_rhythm2_form.save()
            rhythm2_beats_formset.save()

        # POLYRHYTHM SAVING
        pre_commit_poly_form = poly_form.save(commit=False)
        pre_commit_poly_form.rhythm1 = saved_rhythm1_form
        pre_commit_poly_form.rhythm2 = saved_rhythm2_form
        pre_commit_poly_form.save()

        return redirect('polyrhythm_list')


class PolyrhythmDisplay(View):

    def get(self, request, poly_id):
        poly_array = []

        poly = Polyrhythm.objects.get(id = poly_id)
        rhythm1 = poly.rhythm1
        rhythm2 = poly.rhythm2

        rhythms = [rhythm1, rhythm2]
        poly_length = rhythm1.timing * rhythm2.timing

        # for each beat in polyrhythm
        for a in range(0, poly_length):
            which_sounds = ""

            # for each rhythm
            for b in range(0, 2):
                rhythm = rhythms[b]
                where_in_rhythm =  (a % rhythm.timing) + 1

                beatplay = Beatplay.objects.filter(related_rhythm = rhythm).get(order=where_in_rhythm)
                sounds = Sound.objects.filter(m2m_sound_beatplay__id=beatplay.id)
                for c in range(0, sounds.count()):
                    which_sounds = which_sounds + sounds[c].abbreviation + ", "

            # TODO fix duplication
            poly_array.append([a+1, which_sounds])
        return render(request, 'polyrhythm_display.html', {'poly': poly,
                                                           'poly_array': poly_array
                                                           })
