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


class PolyrhythmForm(View):
    def get(self, request):
        blob = Polyrhythm.objects.get(id=1)
        form_class = PolyrhythmForm(instance=blob)
        print(form_class)
        return render(request, 'polyrhythm_form.html', {'form': form_class})

    def post(self, request):
        blob = None
        form_class = PolyrhythmForm(request.POST, instance=blob)
        if form_class.is_valid():
            form_class.save()
        return redirect('app:polyrhythm_list')
