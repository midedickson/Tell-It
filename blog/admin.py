from django.contrib import admin

from .models import Post, Profile, Image, Comment
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'status', 'category')
    list_filter = ('status', 'created', 'updated')
    search_fields = ('author__username', 'title')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('status', 'category',)
    date_hierarchy = ('created')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date', 'location')

class ImageAdmin(admin.ModelAdmin):
    list_display = ('post', 'image')

admin.site.register(Post, PostAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Comment)