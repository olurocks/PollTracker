from django import forms
from . import models


class AddPollingUnitResultForm(forms.ModelForm):
    class Meta:
        model = models.AnnouncedPuResults
        fields = ['polling_unit_uniqueid', 'party_abbreviation', 'party_score']

class ViewPollResult(forms.ModelForm):
    class Meta:
        model = models.AnnouncedPuResults
        fields = ['polling_unit_uniqueid']
