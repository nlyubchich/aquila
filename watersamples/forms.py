from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from watersamples.models import WaterIntakePoint


class ChartForm(forms.Form):
    date_from = forms.DateField(widget=AdminDateWidget(attrs={'class': 'vDateField fdfdsf'}))
    intake_point = forms.ModelChoiceField(queryset=WaterIntakePoint.objects, widget=forms.Select(attrs={'class': 'form-control required'}))
    info_fields = forms.MultipleChoiceField(choices=[
            ('classification', 'classification'),
            ('smell_20_celsium', 'smell_20_celsium'),
            ('smell_60_celsium', 'smell_60_celsium'),
            ('aftertaste', 'aftertaste'),
            ('color', 'color'),
            ('dry_residue', 'dry_residue'),
            ('pH', 'pH'),
            ('rigidity', 'rigidity'),
            ('nitrates', 'nitrates'),
            ('chlorides', 'chlorides'),
            ('sulphates', 'sulphates'),
            ('iron_overall', 'iron_overall'),
            ('manganese', 'manganese'),
            ('fluorine', 'fluorine'),
        ],
        widget=forms.SelectMultiple(attrs={'class': 'filtered', 'style': 'width: 100%'})
    )
