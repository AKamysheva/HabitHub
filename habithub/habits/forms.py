from django import forms
from .models import Habit, Goal, Remainders

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


class ReminderForm(forms.ModelForm):
    habit = forms.ModelChoiceField(queryset=Habit.objects.none(), empty_label=None, label='Привычка', disabled=True)
    reminder_frequency = forms.ChoiceField(choices=Remainders.FREQUENCY_CHOICES, label='Частота напоминаний', required=False)
    
    class Meta:
        model = Remainders
        fields = ['habit', 'reminder_time', 'reminder_frequency']
        widgets = {
            'habit': forms.Select(attrs={}),
            'reminder_time': forms.TimeInput(attrs={'type': 'time'})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.habit = kwargs.pop('habit', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['habit'].queryset = Habit.objects.filter(user=self.user)
            if self.habit: 
                self.fields['habit'].initial = self.habit

    def clean_reminder_time(self):
        reminder_time = self.cleaned_data['reminder_time']
        if reminder_time:
            reminder_time = reminder_time.replace(second=0, microsecond=0)
        return reminder_time

    def save(self, commit=True): 
        instance = super().save(commit=False) 
        if commit: 
            instance.save() 
        return instance

    


