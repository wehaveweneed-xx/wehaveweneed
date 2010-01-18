from django import forms
from haystack.forms import SearchForm
from wehaveweneed.web.models import Category


class CategoryChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return obj.name


class PostSearchForm(SearchForm):
    """ Our search form.  

    """

    have = forms.BooleanField(initial=True, required=False)
    need = forms.BooleanField(initial=True, required=False)

    category = CategoryChoiceField(queryset=Category.objects.all(),
                                   empty_label='Search in All Categories',
                                   required=False)


    def search(self):
        sqs = super(PostSearchForm, self).search()

        category = self.cleaned_data.get('category')
        if category:
            sqs = sqs.filter(category_id=category.id)

        have = self.cleaned_data['have']
        need = self.cleaned_data['need']
        if have and not need:
            sqs = sqs.filter(type='have')
        if need and not have:
            sqs = sqs.filter(type='need')

        return sqs





