from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import  check_password
from django.http import HttpResponse
from .models import product
from math import ceil
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import Customer
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Contact, Orders, OrderUpdate
import logging
import json
from .models import Prescription

# Create your views here.


def index(request):
    products= product.objects.all()
    n= len(products)
    nSlides= n//4 + ceil((n/4) + (n//4))
    params={'no_of_slides':nSlides, 'range':range(1,nSlides), 'product': products}
    return render(request,"shop/index.html", params)

def about(request): 
    return render(request, 'shop/about.html')

def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content =request.POST['content']
        contact=Contact(name=name, email=email, phone=phone, content=content)
        contact.save()
        messages.success(request, "Your message has been sent")
    return render(request, "shop/contact.html")

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')

def search(request):
    query = request.GET.get('query', '')
    if query:
        results = product.objects.filter(
            Q(product_name__icontains=query) | 
            Q(desc__icontains=query)
        ).distinct()
    else:
        results = []
    
    context = {
        'query': query,
        'results': results
    }
    return render(request, 'shop/search.html', context)

def productView(request, myid):
    products = product.objects.filter(id=myid)
    return render(request, "shop/prodView.html", {'product':products[0]})

def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
    return render(request, 'shop/checkout.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.views import View

class Signup(View):
    def get(self, request):
        return render(request, 'shop/signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        user = User(
            first_name=first_name,
            last_name=last_name,
            username=email,
            email=email,
            password=make_password(password)
        )

        if not error_message:
            user.save()
            login(request, user)
            return redirect('/shop')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'shop/signup.html', data)

class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'shop/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        error_message = None
        if user:
            login(request, user)
            if Login.return_url:
                return redirect(Login.return_url)
            else:
                Login.return_url = None
                return redirect('/shop/')
        else:
            error_message = 'Email or Password invalid !!'
        return render(request, 'shop/login.html', {'error': error_message})

def logout_view(request):
    logout(request)
    return redirect('/shop/')

def uploadPres(request):
    if request.method == 'POST':
        prescription_file = request.FILES.get('prescription_file')
        if prescription_file:
            # Save the uploaded file or process it as needed
            # Example: Saving the prescription file to a model
            prescription = Prescription(file=prescription_file)
            prescription.save()
            messages.success(request, 'Prescription uploaded successfully.')
            return redirect('shop/')
        else:
            messages.error(request, 'No file selected.')
    
    return render(request, 'shop/uploadPres.html')