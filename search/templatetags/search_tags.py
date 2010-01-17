from django import template
from wehaveweneed.search.forms import PostSearchForm

register = template.Library()


@register.inclusion_tag('search/search_bar.html')
def search_bar():
    return {'form': PostSearchForm()}
