from django import template
from habits.utils import menu_first, menu_second

register = template.Library()

@register.simple_tag
def get_menu():
    return menu_first

@register.simple_tag
def get_menu2():
    return menu_second