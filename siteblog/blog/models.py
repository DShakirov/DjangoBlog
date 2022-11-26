from django.contrib.auth.models import User
from django.db import models
from django.http import request
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
from autoslug import AutoSlugField


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Категория')
    slug = models.SlugField(max_length=250, verbose_name='URL', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['title']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Tag(models.Model):
    title = models.CharField(max_length=150, verbose_name='Тег')
    slug = models.SlugField(max_length=250, verbose_name='URL', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['title']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Post(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    slug = AutoSlugField(populate_from='title', unique_with='created_at')
    author = models.CharField(max_length=250, verbose_name='Автор', blank=True)
    #author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE, default=1, blank=True, null=True)
    on_top = models.BooleanField(default=False, verbose_name='Закрепленная запись')
    photo = models.ImageField(verbose_name='Изображение', blank=True)
    content = CKEditor5Field('Текст', config_name='extends')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    views = models.IntegerField(default=0, verbose_name='Просмотров')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts', verbose_name='Категория')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name='Теги')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})


    class Meta:

        ordering = ['-on_top', '-created_at']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50, verbose_name='Автор')
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return 'Comment on {} by {}'.format(self.name, self.post)


