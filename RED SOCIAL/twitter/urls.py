from django.urls import path
from .views import home,register,delete,profile,editar,follow
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [
    path('',home,name="home"),
    path('register/',register,name="register"),
    path('login/',LoginView.as_view(template_name='twitter/login.html'),name="login"),
    path('logout/',LogoutView.as_view(),name="logout"),
    path('delete <int:id_post>',delete,name="delete"),
    path('profile/<str:username>',profile,name="profile"),
    path('editar/',editar,name="editar"),
    path('follow/<str:username>',follow,name='follow'),
    
]
