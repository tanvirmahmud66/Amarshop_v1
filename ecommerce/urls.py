from django.urls import path
from . import views

urlpatterns = [
    path('',views.Home,name='amarshop'),
    path('products/',views.Products,name='products'),
    path('products/<int:product_code>/<str:product_name>/',views.ProductDetails, name='product-details'),
    path('cart/',views.Cart,name='cart'),
    path('login/',views.Login,name='login'),
    path('singup/',views.Signup,name='signup'),
]