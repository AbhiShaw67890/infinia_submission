from django.urls import path
from . import views

app_name = 'items'

urlpatterns = [
    path('',               views.feed_view,        name='feed'),
    path('search/',        views.search_view,       name='search'),
    path('<int:pk>/',      views.item_detail_view,  name='detail'),
    path('create/',        views.create_item_view,  name='create'),
    path('<int:pk>/edit/', views.edit_item_view,    name='edit'),
    path('<int:pk>/delete/', views.delete_item_view, name='delete'),
    path('my-posts/',      views.my_posts_view,     name='my_posts'),
]
