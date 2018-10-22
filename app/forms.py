from django.forms import Form, ModelForm, formset_factory, IntegerField
from app.models import Polyrhythm, Rhythm, Sound


class PolyrhythmForm(ModelForm):

    class Meta:
        model = Polyrhythm
        fields = ['name', 'description']


class RhythmForm(ModelForm):

    class Meta:
        model = Rhythm
        fields = ['name']

# RhythmFormSet = formset_factory(RhythmForm)
