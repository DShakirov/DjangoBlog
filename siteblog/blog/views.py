from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Q
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import FormMixin, CreateView

from .forms import UserRegisterForm, UserLoginForm, CommentForm, UserAddPostForm
from .models import *


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'blog/login.html', {'form': form})


def user_logout(request):
    logout(request)

    return redirect('login')


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})




class PostHome(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Shakirov's Blog"
        return context

    def get_queryset(self):
        return Post.objects.filter().select_related('category')


class PostsByCategory(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 3
    allow_empty = True

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])


class GetPost(DetailView, FormMixin):
    model = Post
    form_class = CommentForm
    template_name = 'blog/post-details.html'
    context_object_name = 'post'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Post.objects.get(slug=self.kwargs['slug'])
        context['form'] = self.get_form()
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context

    def get_success_url(self):
        return reverse_lazy('post', kwargs={'slug': self.object.slug})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        post = Post.objects.get(slug=self.object.slug)
        form.instance.post = post
        if form.is_valid():
            comment = form.save()
            comment.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)




class PostsByTag(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 5
    allow_empty = True

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])


class GetSearchResults(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 5
    allow_empty = True

    def get_queryset(self):

        query = self.request.GET.get('q')
        if query is not None:
            object_list = Post.objects.filter(Q(title__iregex=query) | Q(content__iregex=query))
            return object_list


class AddPost(LoginRequiredMixin, CreateView):
    form_class = UserAddPostForm
    template_name = 'blog/add_post.html'
    login_url = '/admin'





def page_not_found(request, exception):
    return HttpResponseNotFound('Страница не найдена')
