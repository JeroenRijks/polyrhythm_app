# from django.forms import Form, ModelForm, formset_factory, IntegerField, CharField
from django import forms
from app.models import Polyrhythm, Rhythm, Sound


class PolyrhythmForm(forms.ModelForm):

    class Meta:
        model = Polyrhythm
        fields = ['name', 'description', 'rhythm1', 'rhythm2']


# class RhythmForm(forms.ModelForm):
#
#     class Meta:
#         model = Rhythm
#         fields = ['name']

# RhythmFormSet = formset_factory(RhythmForm)
