from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from django_ckeditor_5.fields import CKEditor5Field
from .models import *


#class PostAdminForm(forms.ModelForm):
   # content = forms.CharField(widget=CKEditor5Field())

 #   class Meta:
   #     model = Post
   #     fields = '__all__'


class PostAdmin(admin.ModelAdmin):

    save_on_top = True
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['id', 'title', 'slug', 'category', 'created_at', 'get_photo', 'on_top', 'views']
    list_display_links = ['id', 'title', 'slug']
    search_fields = ['title']
    list_filter = ['created_at', 'category', 'tags']
    fields = ['title', 'slug', 'category', 'tags', 'content', 'photo', 'get_photo', 'views', 'created_at', 'author',
              'on_top']
    readonly_fields = ['get_photo', 'created_at', 'views']

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')
        else:
            return ('Фото не установлено.')

    get_photo.short_description = 'Миниатюра'


class CategoryAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('title',)}
    list_display = ['id', 'title']
    list_display_links = ['id', 'title']
    search_fields = ['title', ]


class TagAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('title',)}
    list_display = ['id', 'title']
    list_display_links = ['id', 'title']
    search_fields = ['title', ]


class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created_at']
    list_filter = ['created_at']
    search_display = ['name', 'email', 'content']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)


