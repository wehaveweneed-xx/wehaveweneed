from django import forms
from haystack.forms import SearchForm

class PostSearchForm(SearchForm):
    sources = forms.CharField(required=False)

    def search(self):
        sqs = super(PostSearchForm, self).search()

        sources = self.cleaned_data.get('sources')
        if sources and sources != 'all':
            sqs = sqs.filter(category_id=int(sources))

        return sqs
