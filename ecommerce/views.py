from django.shortcuts import render
from app.models import User, Customer, Product, Product_Image
from .models import *
# Create your views here.

def Home(request):
    products = Product.objects.all()[:8]
    return render(request, 'Home.html',{
        "products":products,
    })


def Products(request):
    products = Product.objects.filter(quantity__gt=0)
    return render(request,'Products.html',{
        "products":products
    })



def ProductDetails(request, product_code,product_name):
    product = Product.objects.filter(product_code = product_code).first()
    images = Product_Image.objects.filter(product=product)    
    return render(request,'ProductDetails.html',{
        "product":product,
        "images":images,
    })



def Login(request):
    return render(request, 'Login.html',{})


def Signup(request):
    return render(request, 'Signup.html',{})


def Cart(request):
    return render(request, 'Cart.html',{})