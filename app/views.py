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


class VariableAssignmentView(View):
    poly = None
    rhythm1 = None
    rhythm2 = None

    def assign_values(self, poly_id=None):
        self.poly = Polyrhythm.objects.get(id=poly_id)
        self.rhythm1 = self.poly.rhythm1
        self.rhythm2 = self.poly.rhythm2


class RhythmsEdit(VariableAssignmentView):
    poly_form = None
    rhythm1_form = None
    rhythm2_form = None

    def get(self, request, poly_id=None):
        template = 'rhythms_form.html'
        if poly_id:
            self.assign_values(poly_id)
        self.load_forms()
        return render(request, template, {'poly_form': self.poly_form,
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

    def load_forms(self):
        self.poly_form = PolyrhythmForm(instance=self.poly)
        self.rhythm1_form = RhythmForm(instance=self.rhythm1, prefix='r1')
        self.rhythm2_form = RhythmForm(instance=self.rhythm2, prefix='r2')

    def get_posted_forms(self, request):
        self.rhythm1_form = RhythmForm(request.POST, instance=self.rhythm1, prefix='r1')
        self.rhythm2_form = RhythmForm(request.POST, instance=self.rhythm2, prefix='r2')
        self.poly_form = PolyrhythmForm(request.POST, instance=self.poly)

    def save_forms(self):
        self.save_valid_rhythm_forms()
        self.save_polyrhythm_form()

    def create_beatplays(self):
        rhythm_forms = [self.saved_rhythm1_form, self.saved_rhythm2_form]
        for rhythm in rhythm_forms:
            for beat in xrange(0, rhythm.timing):
                beatplay= Beatplay()
                beatplay.order = beat+1
                beatplay.related_rhythm = rhythm
                beatplay.save()

    def save_valid_rhythm_forms(self):
        if self.rhythm1_form.is_valid():
            self.saved_rhythm1_form = self.rhythm1_form.save()
        if self.rhythm2_form.is_valid():
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


class BeatsEdit(VariableAssignmentView):
    rhythm1_beats_formset = None
    rhythm2_beats_formset = None

    def get(self, request, poly_id=None):
        if poly_id:
            self.assign_values(poly_id)
        self.load_formsets()
        return render(request, 'beatplay_formsets.html', {'rhythm1_beats_formset': self.rhythm1_beats_formset,
                                                          'rhythm2_beats_formset': self.rhythm2_beats_formset,
                                                          })

    def post(self, request, poly_id):
        if poly_id:
            self.assign_values(poly_id)
        self.get_posted_formsets(request)
        self.save_valid_formsets()
        return redirect('polyrhythm_list')

    def load_formsets(self):
        self.rhythm1_beats_formset = Rhythm1BeatplayFormSet(instance=self.rhythm1, prefix='r1')
        self.rhythm2_beats_formset = Rhythm2BeatplayFormSet(instance=self.rhythm2, prefix='r2')

    def get_posted_formsets(self, request):
        self.rhythm1_beats_formset = Rhythm1BeatplayFormSet(request.POST, instance=self.rhythm1, prefix='r1')
        self.rhythm2_beats_formset = Rhythm2BeatplayFormSet(request.POST, instance=self.rhythm2, prefix='r2')

    def save_valid_formsets(self):
        formsets = [self.rhythm1_beats_formset, self.rhythm2_beats_formset]
        for formset in formsets:
            if formset.is_valid():
                formset.save()


class PolyrhythmDisplay(VariableAssignmentView):
    poly_array = []

    def assign_values(self, poly_id=None):
        super(PolyrhythmDisplay, self).assign_values(poly_id)
        self.rhythms = [self.rhythm1, self.rhythm2]

    def get(self, request, poly_id):
        self.assign_values(poly_id)
        poly_length = self.rhythm1.timing * self.rhythm2.timing

        for beat in range(0, poly_length):
            self.add_sounds_to_current_beat(beat)
        return render(request, 'polyrhythm_display.html', {'poly': self.poly,
                                                           'poly_array': self.poly_array
                                                           })

    def add_sounds_to_current_beat(self, beat):
        self.current_beat_sounds = []
        for rhythm in self.rhythms:
            self.add_rhythm_sounds_to_beat(beat, rhythm)
        self.poly_array.append([beat + 1, self.current_beat_sounds])

    def add_rhythm_sounds_to_beat(self, beat, rhythm):
        where_in_rhythm = (beat % rhythm.timing) + 1
        current_beatplay = Beatplay.objects.filter(related_rhythm=rhythm).get(order=where_in_rhythm)
        sounds_in_beatplay = Sound.objects.filter(m2m_sound_beatplay__id=current_beatplay.id)
        for sound in sounds_in_beatplay:
            self.add_non_duplicate_sounds_to_beat(sound)

    def add_non_duplicate_sounds_to_beat(self, sound):
            if sound not in self.current_beat_sounds:
                self.current_beat_sounds.append(sound)


