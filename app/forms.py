from django.forms import ModelForm, inlineformset_factory, BaseInlineFormSet
from app.models import Polyrhythm, Rhythm, Sound, Beatplay


class PolyrhythmForm(ModelForm):

    class Meta:
        model = Polyrhythm
        fields = ['poly_name', 'description']


class RhythmForm(ModelForm):

    class Meta:
        model = Rhythm
        fields = ['rhythm_name', 'timing']


class BeatplayForm(ModelForm):

    class Meta:
        model = Beatplay
        fields = ['sounds']

Rhythm1BeatplayFormSet = inlineformset_factory(Rhythm,
                                        Beatplay,
                                        form=BeatplayForm,
                                        extra=0)

Rhythm2BeatplayFormSet = inlineformset_factory(Rhythm,
                                        Beatplay,
                                        form=BeatplayForm,
                                        extra=0)
