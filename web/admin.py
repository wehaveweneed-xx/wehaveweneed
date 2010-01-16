from django.contrib import admin
from wehaveweneed.web.models import Category, Post

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title','slug')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post)