from django.forms import ModelForm, inlineformset_factory, BaseInlineFormSet
from app.models import Polyrhythm, Rhythm, Sound, Beatplay


class PolyrhythmForm(ModelForm):

    class Meta:
        model = Polyrhythm
        fields = ['poly_name', 'description']


class RhythmForm(ModelForm):

    class Meta:
        model = Rhythm
        fields = ['rhythm_name']


class BeatplayForm(ModelForm):
    class Meta:
        model = Beatplay
        fields = ['sounds','order','related_rhythm']

BeatplayFormSet = inlineformset_factory(Rhythm,
                                        Beatplay,
                                        form=BeatplayForm,
                                        extra=1)
Rhythm1BeatplayFormSet = inlineformset_factory(Rhythm,
                                        Beatplay,
                                        form=BeatplayForm,
                                        extra=2)
Rhythm2BeatplayFormSet = inlineformset_factory(Rhythm,
                                        Beatplay,
                                        form=BeatplayForm,
                                        extra=3)
