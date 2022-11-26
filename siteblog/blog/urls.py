from django.urls import path, include
from .views import *



urlpatterns = [
    
    path('', PostHome.as_view(), name='home'),
    path('post/<str:slug>/', GetPost.as_view(), name='post'),
    path('cats/<str:slug>/', PostsByCategory.as_view(), name='category'),
    path('tag/<str:slug>/', PostsByTag.as_view(), name='tag'),
    path('search/', GetSearchResults.as_view(), name='search'),
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('add_post/', AddPost.as_view(), name='add_post')

    
]

handler404 = page_not_found

