from django.urls import path
from . import views

urlpatterns = [
    path('', views.hub, name="hub"),
    path('register_user/', views.registerUserPage, name="registerUserPage"),
    path('register_employer/', views.registerEmployerPage, name="registerEmployerPage"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('account/', views.account, name="account"),
    path('datapool/<str:pk>/', views.datapool, name="datapool"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('references/', views.references, name="references"),
    path('create_datapool/', views.createDataPool, name="createDataPool"),
    path('download/<str:pk>/', views.download, name="download"),
    path('welcome/', views.welcome, name='welcome')
]