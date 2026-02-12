

from django.urls import path

from . import views
# from .views import cart


urlpatterns = [
    path('register/', views.register,name='register'),
    path('login/', views.login,name='login'),
    path('logout/', views.logout,name='logout'), 
    path('dashboard/', views.dashboard,name='dashboard'), 
    path('', views.dashboard,name='dashboard'),


    path('activate/<uidb64>/<token>/',views.activate,name='activate'), 
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate,name='resetpassword_validate'), 
    path('resetPassword/', views.resetPassword, name='resetPassword'),


    path('my_orders/',views.my_orders,name='my_orders'),
    path('edit_profiles/',views.edit_profiles,name='edit_profiles'),
    path('change_password/',views.change_password,name='change_password'),
    path('order_details/<int:order_id>/',views.order_details,name='order_details'),
]