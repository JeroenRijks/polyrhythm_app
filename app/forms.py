from django.forms import ModelForm, inlineformset_factory
from app.models import Polyrhythm, Rhythm, Sound, Beatplay


class PolyrhythmForm(ModelForm):

    class Meta:
        model = Polyrhythm
        fields = ['name', 'description']


class RhythmForm(ModelForm):

    class Meta:
        model = Rhythm
        fields = ['name']


# RhythmFormSet = inlineformset_factory(Polyrhythm, Rhythm, fields=('name',))
BeatplayFormSet = inlineformset_factory(Rhythm, Beatplay, fields=('order',))