from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.AboutView.as_view(), name='about'),
    path('credentials/', views.CredentialsView.as_view(), name='credentials'),
    path('works/', views.WorksView.as_view(), name='works'),
    path('works/<slug:slug>/', views.WorksDetailView.as_view(), name='works-detail'),
    path('service/', views.service_page, name='service'),

]
