from django import forms
from .models import Tournament


class TournamentCreateForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ('name', 'description', 'max_participants', 'prize_pool', 'start_date', 'end_date')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError('End date must be after start date.')

        return cleaned_data