from django.urls import path,include
from . import views



app_name = 'rideservice'
urlpatterns = [
    path(r'index/', views.index, name='index'),
    path(r'login/', views.login, name='login'),
    path(r'register/', views.register, name='register'),
    path(r'logout/', views.logout, name='logout'),
    path(r'my/', views.my, name='my'),
    path(r'edit/', views.edit, name='edit'),
    path(r'editcar/', views.editcar, name='editcar'),
    path(r'bedriver/', views.bedriver, name='bedriver'),
    path(r'd_list/', views.d_viewlist, name='d_viewlist'),
    path(r'd_list/<ride_id>/', views.d_viewdetail, name='ride_detail'),
    path(r'd_list/complete/<ride_id>/', views.d_viewcomplete, name='ride_complete'),
    path(r'd_list/confirm/<ride_id>/', views.d_viewconfirm, name='ride_confirm'),
    path(r'd_search/', views.d_search, name='d_search'),

    path(r'riderequest/', views.riderequest, name='riderequest'),
    path(r'u_list/', views.u_viewlist, name='u_list'),
    path(r'u_list/<ride_id>/', views.u_viewdetail, name='u_viewdetail'),
    path(r'u_list/edit/<ride_id>/', views.u_edit, name='u_edit'),
    path(r'u_search/', views.u_search, name='u_search'),
    path(r'u_search/join/<ride_id>/<number_you>/', views.join, name='join'),

]