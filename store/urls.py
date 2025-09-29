

from django.urls import path

from store import views


urlpatterns = [
   
    path('', views.store,name='store'),
    #to accept the categoryslug in the link
    path('<slug:category_slug>/', views.store,name='product_by_category'),
    #to accept the product slug in the link
    path('<slug:category_slug>/<slug:product_slug>/', views.product_details,name='product_details'),
]