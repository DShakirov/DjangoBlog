from django import template
from blog.models import Category

register = template.Library()


@register.inclusion_tag('blog/menu_tpl.html')
def show_menu(menu_class='collapse navbar-collapse'):
    categories = Category.objects.all()
    return {'categories': categories, 'menu_class': menu_class}


@register.inclusion_tag('blog/menu_tpl_footer.html')
def show_menu_footer(menu_class='container'):
    categories = Category.objects.all()
    return {'categories': categories, 'menu_class_footer': menu_class}