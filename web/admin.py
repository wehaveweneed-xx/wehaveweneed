from django.contrib import admin
from wehaveweneed.web.models import UserProfile, Post, Category, Reply

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name','slug')

admin.site.register(Category, CategoryAdmin)
admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Reply)
