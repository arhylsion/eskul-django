from django.urls import path
from . import views

urlpatterns = [
    path('form/', views.registration_form, name='registration_form'),
]
