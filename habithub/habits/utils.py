import csv

menu_first = [{'title': 'HabitHub', 'url_name': 'home'}]

menu_second = [{'title':'Привычки', 'url_name': 'habits'}, 
               {'title':'Цели', 'url_name': 'goals'}, 
               {'title':'Прогресс', 'url_name': 'progress'},
               {'title':'Обратная связь', 'url_name':'feedback'}]

class DataMixin:
    def get_mixin_context(self, context, **kwargs):
        context['menu_first'] = menu_first
        context['menu_second'] = menu_second
        context.update(kwargs)
        return context
    
def get_lst_habits(file_path):
    lst_habits = []
    with open(file_path, encoding='utf-8', newline='') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            lst_habits.append(row['Название привычки'])
    return lst_habits