from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import json
from app.models import User, Customer, Product, Product_Image
from .models import *
from .forms import *
# Create your views here.


#============================================================= Login View 
def Login(request):
    error=None
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request,user)
        else:
            error = "Invalid Email or Password"
    return render(request, 'Login.html',{
        "error":error
    })


def Logout(request):
    logout(request)
    return redirect('login')


#============================================================= Registration View 
def Registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            customer = Customer.objects.create(user=user, email=email)
            customer.save()
            print(user)
            login(request,user)
            return redirect('amarshop')  # You can redirect to any URL you prefer after successful signup
    else:
        form = SignUpForm()
    return render(request, 'Registration.html',{
        "form": form
    })


#============================================================= Forget Password View 
def Forget_password(request):
    return render(request,'ForgetPassword.html',{})



#============================================================= Home View 
def Home(request):
    products = Product.objects.all()[:8]
    return render(request, 'Home.html',{
        "products":products,
    })


#============================================================= Products View 
def Products(request):
    products = Product.objects.filter(quantity__gt=0)
    return render(request,'Products.html',{
        "products":products
    })


#============================================================= ProductDetails View 
def ProductDetails(request, product_code,product_name):
    product = Product.objects.filter(product_code = product_code).first()
    images = Product_Image.objects.filter(product=product)    
    return render(request,'ProductDetails.html',{
        "product":product,
        "images":images,
    })


#============================================================= Cart View 
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


# ============================================================ Update Item
def UpdateItem(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']
    quantity = data['quantity']
    get_product = Product.objects.filter(id=product_id).first()
    customer = request.user.customer
    order,created =  Order.objects.get_or_create(customer, complete=False)
    orderItem, created = OrderItems.objects.get_or_create(order=order, product=get_product)
    if action =='add' and orderItem.quantity<orderItem.product.quantity:
        orderItem.quantity += int(quantity)
    elif action =='remove':
        orderItem.quantity -= 1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse("Item was Added...",safe=False)


#============================================================= Checkout View 
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


