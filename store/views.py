from django.shortcuts import render, redirect
from razorpay.resources import payment
from .models import *
from django.http import JsonResponse, HttpResponse
import json
import datetime
from django.utils import timezone
from .utils import cookieCart, cartData
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from django.views.decorators.csrf import csrf_exempt
import razorpay

def mens(request):
    data = cartData(request)

    cartItems = data['cartItems']

    products = Product.objects.all()
    
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/mens.html', context)


def menformal(request):
    data = cartData(request)

    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/menformal.html', context)

def mencasual(request):
    data = cartData(request)

    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/mencasual.html', context)

def mensports(request):
    data = cartData(request)

    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/mensports.html', context)


def menchappal(request):
    data = cartData(request)

    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/menchappal.html', context)


def wcasual(request):
    data = cartData(request)

    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/wcasual.html', context)


def wsports(request):
    data = cartData(request)

    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/wsports.html', context)


def wslippers(request):
    data = cartData(request)

    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/wslippers.html', context)



def kcasual(request):
    data = cartData(request)

    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/kcasual.html', context)



def ksandal(request):
    data = cartData(request)

    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/ksandal.html', context)



def contactus(request):
    data = cartData(request)
    cartItems = data['cartItems']
    context = {'cartItems': cartItems}
    thank = False
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')

        if len(phone) != 10:
            messages.error(request, "Please enter 10 digit phone number")
            return redirect('contactus')


        contactus = Contactus(name=name, email=email, phone=phone, desc=desc)
        contactus.save()
        thank = True
        messages.success(request, "Thanks for contacting us! We will get back to you soon!")
        return redirect('scart')
        
    else:
        data = cartData(request)
        cartItems = data['cartItems']
        context = {'cartItems': cartItems}
        return render(request, 'store/contactus.html', context)
    return render(request,'store/contactus.html',{'thank': thank})

def aboutus(request):
    data = cartData(request)
    cartItems = data['cartItems']
    context = {'cartItems': cartItems}

    return render(request, 'store/aboutus.html', context)

@csrf_exempt
def scart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    context = {'cartItems': cartItems}
    return render(request, 'store/index.html', context)

def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    cust = request.user.customer
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items,'order':order,'cartItems':cartItems,'cust':cust}
    return render(request,'store/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:',action)
    print('productId:',productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(customer=customer,order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    
    transaction_id = datetime.datetime.now()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    total = float(data['form']['total'])
   
    order.transaction_id=transaction_id
    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
    return JsonResponse('Payment Complete!', safe=False)

def register(request):
    data = cartData(request)
    cartItems = data['cartItems']
    customer = Customer.objects.all()
    context = {'cartItems': cartItems}
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        register.email=request.POST['email']
        register.fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        for cust in customer:
            if cust.user.username ==  username:
                messages.error(request, "Username already exist,please try another username")
                return redirect('register')
        if len(pass1) < 6 :
            messages.error(request, "password must be atleast 6 characters long")
            return redirect('register')
        for cust in customer:
            if cust.email == register.email:
                messages.error(request,"email id already exist,try another email id")
                return redirect('register')
        # check for errorneous input
        if len(username)>10:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('register')

        if not register.fname.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('register')

        if not lname.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('register')

        if len(pass1) > 8:
            messages.error(request, "Please enter password less than 8 chracters")

        if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
             return redirect('register')


        # Create the user
        myuser = User.objects.create_user(username, register.email, pass1)
        myuser.first_name= register.fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request, " Your account has been successfully created")
        return redirect('scart')
        


    else:
       return render(request, 'store/register.html')
    return render(request, 'store/register.html', {'myuser':myuser},context)
    
def ulogin(request):
    data = cartData(request)
    cartItems = data['cartItems']
    context = {'cartItems': cartItems}
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("scart")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("ulogin")
    else:
         return render(request, 'store/ulogin.html',context)
   

    return HttpResponse("login")

def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('scart')

@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile') 
def save_profile(sender, instance, created, **kwargs): 
    user = instance 
    if created: 
        profile = Customer(user=user,name=register.fname,email=register.email) 
        profile.save()

def myorder(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    cust=request.user.customer
    orderitem = OrderItem.objects.all()
    product=Product.objects.all()
    context = {'cust':cust,'orderitem':orderitem,'products':product,'cartItems': cartItems, 'order':order, 'items':items}
    return render(request, 'store/myorder.html', context)

def search(request):
    data=cartData(request)
    cartItems=data['cartItems']
    query=request.GET['query']
    
    if len(query)>78 :
        product=Product.objects.none()
        messages.warning(request, "No search results found. Please refine your query.")  
    else:
        product_name= Product.objects.filter(name__icontains=query)
        product_price= Product.objects.filter(price__icontains=query)
        product=product_name.union(product_price)
        if product.count()==0:
            messages.warning(request, "No search results found. Please refine your query.")
    context={'products': product,'cartItems':cartItems}
    return render(request, 'store/search.html', context)

