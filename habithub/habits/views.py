from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic import ListView, CreateView, FormView
from .models import *
from .forms import AddHabitForm, AddGoalForm, FeedbackForm
from habits.utils import DataMixin, get_lst_habits
from django.core.mail import send_mail
import plotly.graph_objects as px
from plotly.offline import plot
from datetime import datetime, timedelta
import json



class HomePageView(DataMixin, TemplateView):
    template_name = 'habits/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_habits = self.request.user.habit_set.all()
            habit_names = [i.name for i in user_habits]
            context['habit_chart'] = self.create_habit_chart(habit_names)
        else:
            context['habit_chart'] = None
        return self.get_mixin_context(context, title='Главная страница')
    
    def create_habit_chart(self, habit_names):
        fig = px.Figure(px.Pie(
            labels=habit_names,
            values=[1] * len(habit_names),
            textinfo='label',
            hoverinfo='none'
        ))
        fig.update_traces(textfont=dict(color="white"))
        fig.update_layout(font=dict(family='CormorantGaramond-Regular', size=16), showlegend=False)
        return fig.to_html(full_html=False)

class HabitsView(DataMixin, ListView):
    template_name = 'habits/habits.html'
    context_object_name = 'habits'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            filter_option = self.request.GET.get('filter', 'all')
            if filter_option == 'all':
                return Habit.objects.filter(user=self.request.user, status__in=[Habit.Status.ACTIVE, Habit.Status.COMPLETED])
            else:
                return Habit.objects.filter(user=self.request.user, status=Habit.Status.ARCHIVED)
        else:
            return Habit.objects.none() 
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_option'] = self.request.GET.get('filter', 'all') 
        return self.get_mixin_context(context, title='Привычки')


class AddHabit(LoginRequiredMixin, DataMixin, CreateView):
    model = Habit
    form_class = AddHabitForm
    template_name = 'habits/add-habit.html'
    success_url = reverse_lazy('habits')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lst_habits = get_lst_habits('C:/Python/Django/my_second_site/habithub/habits/static/habits/documents/lst_habits.csv')
        lst_frequancy = ['Ежедневно', '1 раз в неделю', 'Несколько раз в неделю', 'Несколько раз в месяц']
        context['lst_habits'] = lst_habits
        context['lst_frequancy'] = lst_frequancy
        return self.get_mixin_context(context, title='Добавление привычки')
    
    def form_valid(self, form):
        post_data = self.request.POST.copy() 
        if 'habit_choice' in post_data:
            if post_data['habit_choice'] == 'other': 
                form.cleaned_data['name'] = post_data['custom_name'] 
            else: 
                form.cleaned_data['name'] = post_data['habit_choice']
        if 'frequency_choice' in post_data:
            if post_data['frequency_choice'] == 'other': 
                form.cleaned_data['frequency'] = post_data['custom_frequency'] 
            else: 
                form.cleaned_data['frequency'] = post_data['frequency_choice']
                
        habit = form.save(commit=False)
        habit.user = self.request.user
        habit.save()
        return super().form_valid(form)



def archivehabit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    habit.status = Habit.Status.ARCHIVED
    habit.save()
    return redirect('habits')

def delete_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    habit.delete()
    return redirect('habits')

def restore_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user= request.user)
    habit.status = Habit.Status.ACTIVE
    habit.save()
    return redirect('habits')


class GoalsView(DataMixin, ListView):
    template_name = 'habits/goals_lst.html'
    context_object_name = 'goals'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            filter_option = self.request.GET.get('filter', 'all')
            if filter_option == 'all':
                goals = Goal.objects.filter(user=self.request.user, status__in=[Goal.Status.ACTIVE, Goal.Status.COMPLETED])
            else:
                goals = Goal.objects.filter(user=self.request.user, status=Goal.Status.ARCHIVED)
            
            for goal in goals:
                goal.update_status()

            return goals
        else:
            return Goal.objects.none() 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_option'] = self.request.GET.get('filter', 'all') 
        return self.get_mixin_context(context, title='Цели')
    
class AddGoal(LoginRequiredMixin, DataMixin, CreateView):
    model = Goal
    form_class = AddGoalForm
    template_name = 'habits/add-goal.html'
    success_url = reverse_lazy('goals')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'user': self.request.user}
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title='Добавление цели')

    def form_valid(self, form):
        goal = form.save(commit=False)
        goal.user = self.request.user
        goal.save()
        return super().form_valid(form)

def archivegoal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    goal.status = Goal.Status.ARCHIVED
    goal.save()
    return redirect('goals')  

def delete_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    goal.delete()
    return redirect('goals')

class ProgressView(DataMixin, TemplateView):
    template_name = 'habits/progress.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            habits = Habit.objects.filter(user=self.request.user, status__in=[Habit.Status.ACTIVE, Habit.Status.COMPLETED])
            goals = Goal.objects.filter(user=self.request.user, status__in=[Goal.Status.ACTIVE, Goal.Status.COMPLETED])
            context['habits'] = habits
            context['goals'] = goals
        else:
            context['habits'] = Habit.objects.none()
            context['goals'] = Goal.objects.none()
        return self.get_mixin_context(context, title='Прогресс')
    

class FeedbackView(LoginRequiredMixin, FormView):
    template_name = 'habits/feedback.html'
    form_class = FeedbackForm
    success_url = reverse_lazy('feedback-answer')

    def form_valid(self, form):
        feedback = form.cleaned_data['feedback']
        email_user = self.request.user.email
        print(email_user)
        send_mail('Обратная связь от пользователя', feedback, email_user, ['tashkina12@gmail.com'], fail_silently=False,)
        return super().form_valid(form)