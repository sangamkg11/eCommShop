

from django.urls import path

from . import views
# from .views import cart


urlpatterns = [
   
    path('', views.cart,name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart,name='add_cart'),
    # path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/', views.remove_cart,name='remove_cart'),
    path('del_cart_item/<int:product_id>/', views.del_cart_item,name='del_cart_item'),
    
    
]