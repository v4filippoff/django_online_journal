from django.contrib import admin

from .models import Post, Comment


class ChoiceInline(admin.TabularInline):
    model = Comment
    extra = 3

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'pub_date', 'is_active']
    list_editable = ['is_active']
    list_filter = ['pub_date']
    search_fields = ['title']

    inlines = [ChoiceInline]


admin.site.register(Post, PostAdmin)
