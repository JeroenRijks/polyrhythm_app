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
        rhythm1_beats_formset = BeatplayFormSet(instance=rhythm1)
        rhythm2_form = RhythmForm(instance=rhythm2)
        rhythm2_beats_formset = BeatplayFormSet(instance=rhythm2)
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
        poly_form = PolyrhythmForm(request.POST, instance=poly)
        rhythm1_form = RhythmForm(request.POST, instance=rhythm1)
        rhythm2_form = RhythmForm(request.POST, instance=rhythm2)
        rhythm1_beats_formset = BeatplayFormSet(request.POST, instance=rhythm1)
        # rhythm2_beats_formset = BeatplayFormSet(request.POST, instance=rhythm2)

        if poly_form.is_valid():
            if rhythm1_form.is_valid():
                if rhythm2_form.is_valid():
                    if rhythm1_beats_formset.is_valid():
                        print("r1 beats formset:")
                        print(rhythm1_beats_formset)
                        # r1bfs = rhythm1_beats_formset.save()
                        # print("r1 beats formset:")
                        # print(r1bfs)
                        # saved_rhythm1_form = rhythm1_form.save()
                        # saved_rhythm2_form = rhythm2_form.save()
                        # pre_commit_poly_form = poly_form.save(commit=False)
                        # pre_commit_poly_form.rhythm1 = saved_rhythm1_form
                        # pre_commit_poly_form.rhythm2 = saved_rhythm2_form
                        # pre_commit_poly_form.save()
        return redirect('polyrhythm_list')



    # def post(self, request, poly_id = None):
    #     poly = None
    #     rhythm1 = None
    #     rhythm2 = None
    #     if poly_id:
    #         poly = Polyrhythm.objects.get(id=poly_id)
    #         rhythm1 = poly.rhythm1
    #         rhythm2 = poly.rhythm2
    #     rhythm1_beats_formset = BeatplayFormSet(request.POST, instance = rhythm1)
    #     if rhythm1_beats_formset.is_valid():
    #         rhythm1_beats_formset.save()
    #         return redirect('app: polyrhythm_list')






