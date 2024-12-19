from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Habit, Goal

class AddHabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'frequency']

    def clean_name(self):
        name = self.cleaned_data['name']
        name = name.capitalize()
        return name
    
    def clean_frequency(self):
        frequency = self.cleaned_data['frequency']
        frequency = frequency.capitalize()
        return frequency
    
class AddGoalForm(forms.ModelForm):
    habit = forms.ModelChoiceField(queryset=Habit.objects.none(), empty_label='Выберите привычку', label='Привычка')

    class Meta:
        model = Goal
        fields = ['habit', 'description', 'target_date']
        widgets = {
            'habit': forms.Select(attrs={}),
            'target_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.initial.get('user')
        if user:
            self.fields['habit'].queryset = Habit.objects.filter(user=user)

class FeedbackForm(forms.Form):
    feedback = forms.CharField(widget=forms.Textarea(attrs={'rows': '4', 'cols': '40', 'placeholder': 'Ваши предложения по улучшению приложения...'}), label='Обатная связь')


        

        



