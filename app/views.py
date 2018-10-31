# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from app.models import Polyrhythm, Rhythm, Beatplay, Sound
from app.forms import PolyrhythmForm, RhythmForm, BeatplayForm, Rhythm1BeatplayFormSet, Rhythm2BeatplayFormSet


class PolyrhythmList(View):
    def get(self, request):
        polys = Polyrhythm.objects.all()
        return render(request, 'polyrhythm_list.html', {'polys': polys})


class RhythmsEdit(View):
    poly = None
    rhythm1 = None
    rhythm2 = None
    poly_form = None
    rhythm1_form = None
    rhythm2_form = None
    template = 'rhythms_form.html'

    def get(self, request, poly_id=None):
        if poly_id:
            self.assign_values(poly_id)
        self.load_forms()
        return render(request, self.template, {'poly_form': self.poly_form,
                                                'rhythm1_form': self.rhythm1_form,
                                                'rhythm2_form': self.rhythm2_form,
                                                })

    def post(self, request, poly_id=None):
        if poly_id:
            self.assign_values(poly_id)
        self.get_posted_forms(request)
        # TODO add validation function
        self.save_forms()
        self.create_beatplays()
        return redirect('beats_edit', poly_id = self.poly_id)

    def assign_values(self, poly_id):
        self.poly = Polyrhythm.objects.get(id=poly_id)
        self.rhythm1 = self.poly.rhythm1
        self.rhythm2 = self.poly.rhythm2

    def load_forms(self):
        self.poly_form = PolyrhythmForm(instance=self.poly)
        self.rhythm1_form = RhythmForm(instance=self.rhythm1, prefix='r1')
        self.rhythm2_form = RhythmForm(instance=self.rhythm2, prefix='r2')

    def get_posted_forms(self, request):
        self.rhythm1_form = RhythmForm(request.POST, instance=self.rhythm1, prefix='r1')
        self.rhythm2_form = RhythmForm(request.POST, instance=self.rhythm2, prefix='r2')
        self.poly_form = PolyrhythmForm(request.POST, instance=self.poly)

    def save_forms(self):
        self.save_rhythm_forms()
        self.save_polyrhythm_form()

    def create_beatplays(self):
        rhythm_forms = [self.saved_rhythm1_form, self.saved_rhythm2_form]
        for rhythm in rhythm_forms:
            for beat in xrange(0, rhythm.timing):
                beatplay= Beatplay()
                beatplay.order = beat+1
                beatplay.related_rhythm = self.saved_rhythm1_form
                beatplay.save()

    def save_rhythm_forms(self):
        self.saved_rhythm1_form = self.rhythm1_form.save()
        self.saved_rhythm2_form = self.rhythm2_form.save()

    def save_polyrhythm_form(self):
        prepared_poly_form = self.attach_rhythms_to_polyrhythm()
        prepared_poly_form.save()
        self.poly_id = prepared_poly_form.id

    def attach_rhythms_to_polyrhythm(self):
        pre_commit_poly_form = self.poly_form.save(commit=False)
        pre_commit_poly_form.rhythm1 = self.saved_rhythm1_form
        pre_commit_poly_form.rhythm2 = self.saved_rhythm2_form
        return pre_commit_poly_form



class BeatsEdit(View):
    def get(self, request, poly_id=None):
        poly = None
        rhythm1 = None
        rhythm2 = None
        if poly_id:
            poly = Polyrhythm.objects.get(id=poly_id)
            rhythm1 = poly.rhythm1
            rhythm2 = poly.rhythm2

        rhythm1_beats_formset = Rhythm1BeatplayFormSet(instance=rhythm1, prefix='r1')
        rhythm2_beats_formset = Rhythm2BeatplayFormSet(instance=rhythm2, prefix='r2')

        return render(request, 'beatplay_formsets.html', {'rhythm1_beats_formset': rhythm1_beats_formset,
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

        rhythm1_beats_formset = Rhythm1BeatplayFormSet(request.POST, instance=rhythm1, prefix='r1')
        if rhythm1_beats_formset.is_valid():
            rhythm1_beats_formset.save()

        # RHYTHM 2 SAVING
        rhythm2_beats_formset = Rhythm2BeatplayFormSet(request.POST, instance=rhythm2, prefix='r2')
        rhythm2_beats_formset.save()
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
        for beat in range(0, poly_length):
            which_sounds = []
            for rhythm in rhythms:
                where_in_rhythm =  (beat % rhythm.timing) + 1
                beatplay = Beatplay.objects.filter(related_rhythm = rhythm).get(order=where_in_rhythm)
                sounds = Sound.objects.filter(m2m_sound_beatplay__id=beatplay.id)
                for sound in sounds:
                    if sound not in which_sounds:
                        which_sounds.append(sound)
            poly_array.append([beat+1, which_sounds])
        return render(request, 'polyrhythm_display.html', {'poly': poly,
                                                           'poly_array': poly_array
                                                           })

