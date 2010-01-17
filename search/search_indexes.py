from haystack import indexes, site
from wehaveweneed.web.models import Post


class PostIndex(indexes.RealTimeSearchIndex):
    """
    We'll include all of the fields for now - most of them could be useful
    for faceting, etc. If index size becomes a problem some of them could
    be dropped.
    """
    text = indexes.CharField(document=True, use_template=True,
                             template_name='search/indexes/post.txt',
                             stored=False)
    created_at = indexes.DateTimeField(model_attr='created_at')
    title = indexes.CharField(model_attr='title')
    type = indexes.CharField(model_attr='type')
    priority = indexes.CharField(model_attr='priority')
    location = indexes.CharField(model_attr='location')
    geostamp = indexes.CharField(model_attr='geostamp', null=True)
    time_start = indexes.DateTimeField(model_attr='time_start', null=True)
    time_end = indexes.DateTimeField(model_attr='time_end', null=True)
    category = indexes.CharField(model_attr='category__name')
    category_id = indexes.IntegerField(model_attr='category_id')
    contact_phone = indexes.CharField(model_attr='contact__phone',
                                     null=True)
    responses = indexes.IntegerField(model_attr='responses')
    fulfilled = indexes.BooleanField(model_attr='fulfilled')


site.register(Post, PostIndex)
