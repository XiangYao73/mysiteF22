from datetime import date, datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import F
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import InterestForm, OrderForm
from .models import Category, Client, Order, Product
from django.contrib.auth.models import User
import hashlib
# Create your views here.

def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]

    if 'last_login' in request.session:
        logininfo = request.session['last_login']
    else:
        logininfo = 'Your last login was more than an hour ago'
    return render(request, 'myapp/index.html', {'cat_list': cat_list, 'logininfo': logininfo})


def about(request):
    if 'about_visits' in request.session:
        last_visit = request.session['about_visits']
        request.session['about_visits'] = last_visit + 1
        request.session.set_expiry(10)
    else:
        request.session['about_visits'] = 1
        last_visit = 0
        request.session.set_expiry(300)
    return render(request, 'myapp/about.html', {'last_visit': last_visit})


def detail(request, cat_no):
    # response = HttpResponse()
    cat_name = get_object_or_404(Category, pk=cat_no)
    catprods = Product.objects.filter(category=cat_no)
    return render(request, 'myapp/detail.html', {'cat_name': cat_name, 'prod_list': catprods})


def products(request):
    prodlist = Product.objects.all().order_by('id')
    return render(request, 'myapp/products.html', {'prodlist': prodlist})


def place_order(request):
    msg = ''
    prodlist = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST, initial={'status_date': date.today(), 'order_status': 'Order Placed'})
        if form.is_valid():
            order = form.save(commit=False)
            if order.num_units <= order.product.stock:
                order.save()
                msg = 'Your order has been placed successfully'
            else:
                msg = 'We do not have sufficient sock to fill your order.'
            return render(request, 'myapp/order_response.html', {'msg': msg})

    else:
        form = OrderForm()
        return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'prodlist': prodlist})


def productdetail(request, prod_id):
    prod = Product.objects.get(pk=prod_id)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['interested'] == 'Yes':
                prod.interested = prod.interested + 1
                print(prod.id)
                prod.save()
                return redirect('/myapp/')
            else:
                return redirect('/myapp/')
    else:
        form = InterestForm()
        return render(request, 'myapp/productdetail.html', {'form': form, 'prod': prod})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                if 'last_login' not in request.session:
                    request.session['last_login'] = str(datetime.now())
                    request.session.set_expiry(3600)
                login(request, user)
                return HttpResponseRedirect(reverse('myapp:myorders'))
            else:
                return HttpResponse('Your account is disabled')
        else:
            return HttpResponse('Invalid Login details')
    else:
        return render(request, 'myapp/login.html')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:index'))


@login_required(login_url='/myapp/login/')
def myorders(request):
    if request.user.is_authenticated:
        try:
            usobjid = Client.objects.get(pk=request.user.id)
            orderset = usobjid.order_set.all()
            # return HttpResponse(orderset)
        except:
            response= HttpResponse()
            heading = '<h2>' + 'This user name is not registered.' + '</h2>'
            response.write(heading)
            button = '<a href="/myapp/">' + 'return to main page' + '</a>'
            response.write(button)
            return response
        return render(request, 'myapp/myorders.html', {'orderset': orderset})
    else:
        return HttpResponse("User not authenticated")


def register(request):
    if request.method == 'POST' and request.POST:
        data = request.POST
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        check = User.objects.filter(username=username).exists()
        if check:
            response = HttpResponse()
            heading = '<h2>' + 'This user name is already used!' + '</h2>'
            response.write(heading)
            button = '<a href="/myapp/register">' + 'return to register page' + '</a>'
            response.write(button)
            return response
        else:
            newuser = Client.objects.create(
                username=username,
                email=email,
                password=password
            )
            newuser.set_password(password)
            newuser.save()
            return HttpResponseRedirect(reverse("myapp:login"))
    return render(request, 'myapp/register.html')