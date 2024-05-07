from django.shortcuts import render
from app.models import User, Customer, Product, Product_Image
from .models import *
# Create your views here.



def Login(request):
    return render(request, 'Login.html',{})


def Registration(request):
    return render(request, 'Registration.html',{})


def Forget_password(request):
    return render(request,'ForgetPassword.html',{})




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



def Cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitems_set.all()
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items":0}

    return render(request, 'Cart.html',{
        "cartItems":items,
        "order":order,
    })


def Checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitems_set.all()
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items":0}
    
    return render(request,'Checkout.html',{
        "cartItems":items,
    })


