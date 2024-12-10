from django.urls import path
from . import views

urlpatterns = [
	path('', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('payment_success/', views.success, name="success"),
    path('api', views.my_api, name="my_api"),
    path('delete-item/', views.delete_item, name='delete_item'),

]