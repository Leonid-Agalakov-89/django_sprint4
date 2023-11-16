from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('rules/', views.Rules.as_view(), name='rules'),
    path('about/', views.About.as_view(), name='about'),
]
