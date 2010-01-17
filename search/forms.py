from django import forms
from haystack.forms import SearchForm

class PostSearchForm(SearchForm):
    sources = forms.CharField(required=False)
    have = forms.BooleanField(initial=True, required=False)
    need = forms.BooleanField(initial=True, required=False)

    def search(self):
        sqs = super(PostSearchForm, self).search()

        sources = self.cleaned_data.get('sources')
        if sources and sources != 'all':
            sqs = sqs.filter(category_id=int(sources))

        have = self.cleaned_data['have']
        need = self.cleaned_data['need']
        if have and not need:
            sqs = sqs.filter(type='have')
        if need and not have:
            sqs = sqs.filter(type='need')

        return sqs
