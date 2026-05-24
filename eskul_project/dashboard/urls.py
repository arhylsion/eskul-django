from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('registrant/', views.dashboard_registrant, name='dashboard_registrant'),
    path('registrant/approve/<int:reg_id>/', views.approve_registrant, name='approve_registrant'),
    path('registrant/retry/<int:result_id>/', views.trigger_retry, name='trigger_retry'),
    path('statistics/', views.dashboard_statistics, name='dashboard_statistics'),
    path('settings/', views.dashboard_settings, name='dashboard_settings'),
    path('export/', views.export_to_excel, name='export_excel'),
]
