from django.forms import ModelForm, inlineformset_factory, BaseInlineFormSet
from app.models import Polyrhythm, Rhythm, Sound, Beatplay


class PolyrhythmForm(ModelForm):

    class Meta:
        model = Polyrhythm
        fields = ['poly_name', 'description']


class RhythmForm(ModelForm):

    class Meta:
        model = Rhythm
        fields = ['name']


class BeatplayForm(ModelForm):
    class Meta:
        model = Beatplay
        fields = ['sounds']

# class BaseBeatplayFormSet(BaseInlineFormSet):
#
#     def add_fields(self, form, index):
#         super(BaseBeatplayFormSet, self).add_fields(form, index)
#         # form.nested line not needed since Beatplay is the lowest form


BeatplayFormSet = inlineformset_factory(Rhythm,
                                        Beatplay,
                                        form=BeatplayForm,
                                        extra=0)