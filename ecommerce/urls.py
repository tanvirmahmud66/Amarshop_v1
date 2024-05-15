from django.urls import path
from . import views

urlpatterns = [
    path('',views.Home,name='amarshop'),
    path('products/',views.Products,name='products'),
    path('products/<int:product_code>/<str:product_name>/',views.ProductDetails, name='product-details'),
    path('cart/',views.Cart,name='cart'),
    path('update-item/',views.UpdateItem,name='update-item'),
    path('cart/easy-checkout/',views.Checkout,name='checkout'),

    path('login/',views.Login,name='login'),
    path('logout/',views.Logout,name='logout'),
    path('registration/',views.Registration,name='registration'),
    path('forget-password/',views.Forget_password,name='forget-password'),
]