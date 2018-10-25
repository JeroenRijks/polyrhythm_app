# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from app.models import Polyrhythm, Rhythm, Beatplay, Sound
from app.forms import PolyrhythmForm, RhythmForm, BeatplayFormSet


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

        rhythm1_form = RhythmForm(request.POST, instance=rhythm1)
        rhythm2_form = RhythmForm(request.POST, instance=rhythm2)
        poly_form = PolyrhythmForm(request.POST, instance=poly)

        # THIS IS MY PROBLEM
        rhythm1_beats_formset = BeatplayFormSet(request.POST, instance=rhythm1)
        for individual_beat_form in rhythm1_beats_formset:
            print("_____printing individual formset form______")
            print(individual_beat_form)
            # test = individual_beat_form.save(commit=False)
            # print("____printing individual formset form precommit")
            # print(test)
        # print("____________rhythm1 beats formset is____________")
        # print(rhythm1_beats_formset)
        # test=rhythm1_beats_formset.save(commit=False)
        # print("____________false committed formset is_________")
        # print(test)




        # CHECK IF ALL THINGS ARE VALID. IF SO, THEN...

        # RHYTHM SAVING
        saved_rhythm1_form = rhythm1_form.save()
        saved_rhythm2_form = rhythm2_form.save()

        # POLYRHYTHM SAVING
        pre_commit_poly_form = poly_form.save(commit=False)
        pre_commit_poly_form.rhythm1 = saved_rhythm1_form
        pre_commit_poly_form.rhythm2 = saved_rhythm2_form
        pre_commit_poly_form.save()

        # RHYTHM1 BEATPLAY FORMSET SAVING
        # pre_commit_rhythm1_beats_formset = rhythm1_beats_formset.save(commit=False)
        # print("____Approaching for loop____")
        # print(pre_commit_rhythm1_beats_formset.length())
        # for individual_beat_form in pre_commit_rhythm1_beats_formset:
        #     print("______IN FOR LOOP_______")
        #     print(individual_beat_form)

        return redirect('polyrhythm_list')


class PolyrhythmDisplay(View):

    def get(self, request, poly_id):
        poly_array = []

        poly = Polyrhythm.objects.get(id = poly_id)
        rhythm1 = poly.rhythm1
        rhythm2 = poly.rhythm2

        rhythms = [rhythm1, rhythm2]
        print("____rhythms[0] name is ", rhythms[0])
        print("____rhythms[1] name is ", rhythms[1])
        poly_length = rhythm1.timing * rhythm2.timing

        # for each beat in polyrhythm
        for a in range(0, poly_length):
            print("POLYBEAT___________next beat in polyrhythm is", (a+1))
            which_sounds = ""

            # for each rhythm
            for b in range(0, 2):
                rhythm = rhythms[b]
                print("RHYTHM_______now in rhythm ", rhythm.rhythm_name)
                where_in_rhythm =  (a % rhythm.timing) + 1

                beatplay = Beatplay.objects.filter(related_rhythm = rhythm).get(order=where_in_rhythm)
                print("we're in beat ", where_in_rhythm, " of rhythm ", rhythm.rhythm_name)
                print("the beatplay ID is ", beatplay.id)
                sounds = Sound.objects.filter(m2m_sound_beatplay__id=beatplay.id)
                for c in range(0, sounds.count()):
                    which_sounds = which_sounds + sounds[c].abbreviation + ", "
                    print("whichsounds is now", which_sounds)

            # TODO fix duplication
            poly_array.append([a+1, which_sounds])
        return render(request, 'polyrhythm_display.html', {'poly': poly,
                                                           'poly_array': poly_array
                                                           })
