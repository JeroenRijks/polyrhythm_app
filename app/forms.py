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


class BeatplayForm(ModelForm):
    class Meta:
        model = Beatplay
        fields = ['sounds']


BeatplayFormSet = inlineformset_factory(Rhythm, Beatplay, form=BeatplayForm, extra=0)