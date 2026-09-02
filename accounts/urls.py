from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('add/', views.add,name = 'add'),
    path('sub/', views.sub,name = 'sub'),
    path('div/', views.div,name = 'div'),
    path('multi/', views.multi,name = 'multi'),
    path('modulus/', views.modulus,name = 'modulus'),
]