from haystack.views import SearchView

class PostSearchView(SearchView):

    def get_results(self):
        # Don't ignore empty query
        return self.form.search()
