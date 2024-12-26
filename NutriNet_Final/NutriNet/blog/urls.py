from django.urls import path
from . import views
from .views import chat_view
urlpatterns = [
    path('', chat_view, name='blog-home'),
    path('glucosegraph/', views.graph, name='glucose-graph'),
    path('about/', views.about, name='blog-about')
]