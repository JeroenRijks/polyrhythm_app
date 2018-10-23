# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from app.models import Polyrhythm
from app.forms import PolyrhythmForm


class PolyrhythmList(View):
    def get(self, request):
        polyrhythms = Polyrhythm.objects.all()
        return render(request, 'polyrhythm_list.html', {'polyrhythms': polyrhythms})


class PolyrhythmEdit(View):
    def get(self, request):
        poly_form = PolyrhythmForm()
        return render(request, 'polyrhythm_form.html', {'poly_form': poly_form})

    def post(self, request):
        poly_form = PolyrhythmForm(request.POST)
        if poly_form.is_valid():
            pass
        return redirect('app:polyrhythm_list')