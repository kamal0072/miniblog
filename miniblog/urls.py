from django.contrib import admin
from django.urls import path
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.login, name='login'),
    path('addpost/', views.addpost, name='addpost'),
    path('updatepost/<int:id>', views.updatepost, name='updatepost'),
    path('deletepost/<int:id>', views.deletepost, name='deletepost'),
]
