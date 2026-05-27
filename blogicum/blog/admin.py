from django.contrib import admin
from .models import Post, Location, Category, Comment
# Register your models here.

admin.site.register(Location)
admin.site.register(Category)
admin.site.register(Comment)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author',
                    'is_published')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content', 'pub_date')
