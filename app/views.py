# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from app.models import Polyrhythm, Rhythm
from app.forms import PolyrhythmForm, RhythmForm, BeatplayFormSet


class PolyrhythmList(View):
    def get(self, request):
        polyrhythms = Polyrhythm.objects.all()
        return render(request, 'polyrhythm_list.html', {'polyrhythms': polyrhythms})


class PolyrhythmEdit(View):
    def get(self, request):
        poly_object = Polyrhythm.objects.get(id=1)
        poly_form = PolyrhythmForm(instance=poly_object)
        rhythm1_form = RhythmForm(instance=poly_object.rhythm1)
        rhythm1_beats_formset = BeatplayFormSet(instance=poly_object.rhythm1)
        rhythm2_form = RhythmForm(instance=poly_object.rhythm2)
        rhythm2_beats_formset = BeatplayFormSet(instance=poly_object.rhythm2)

        return render(request, 'polyrhythm_form.html', {'poly_form': poly_form,
                                                        'rhythm1_form': rhythm1_form,
                                                        'rhythm1_beats_formset': rhythm1_beats_formset,
                                                        'rhythm2_form': rhythm2_form,
                                                        'rhythm2_beats_formset': rhythm2_beats_formset,
                                                        })

    def post(self, request):
        poly_form = PolyrhythmForm(request.POST)
        if poly_form.is_valid():
            pass
        return redirect('app:polyrhythm_list')