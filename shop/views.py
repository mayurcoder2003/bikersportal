from django.shortcuts import render,get_object_or_404,redirect,HttpResponseRedirect,reverse
from .models import Product, Contact, Orders, OrderUpdate, BookMechanic, User_Signup
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
# messages import
from django.contrib import messages
# Auth Imports
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponse
# Class based Views
from django.views.generic.edit import UpdateView

MERCHANT_KEY = '4j0d50Ac_p0hbe_!'

def home(request):
    return render(request,'shop/home.html')

def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)

def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    thank = False
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'shop/contact.html', {'thank': thank})


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
                    response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')


def productView(request, myid):

    # Fetch the product using the id
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/prodView.html', {'product':product[0]})


def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        # return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
        # Request paytm to transfer the amount to your account after payment by user
        param_dict = {

                'MID': 'UPMAqZ31008553913525',
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})

    return render(request, 'shop/checkout.html')


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})

# Book Mechanic
def BookMechanicView(request):
    book = BookMechanic.objects.all()
    return render(request,'mechanic/My_Mechanic.html',context={'book':book})

def BookInnerView(request,pk):
    book = get_object_or_404(BookMechanic,pk=pk)

    return render(request,"mechanic/book_mechanic.html",context={'book':book})


# Login
# Login
def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return redirect('/shop/')
            else:
                return HttpResponse("User is not active")
        else:
            messages.error(request,"Username Or Password is Invaild")
            return redirect('/shop/login/')

    return render(request,'authenticate/login.html')


# Signup
def Signup(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        age = request.POST["age"]
        mobile = request.POST["mobile"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        image = request.FILES['myfiles']

        # New User Account
        new = User(first_name=first_name,last_name=last_name,email=email,username=username)
        new.set_password(password)
        new.save()

        # Optional Information
        extra = User_Signup(image=image,user=new,phone=phone,address=address,age=age,mobile=mobile)
        extra.save()
        return HttpResponseRedirect('/shop/login/')

    return render(request,'authenticate/signup.html')

@login_required
def Logout(request):
    logout(request)
    return HttpResponseRedirect('/shop/login/')

def MyProfile(request):
    user = get_object_or_404(User,pk=request.user.pk)
    return render(request,'authenticate/my_profile.html',context={'user':user})

class UpdateBookMechanic(UpdateView):
    model = BookMechanic
    context_object_name = 'mec'
    fields = ['mec_img','name','age','experience','phone','address']
    template_name = 'mechanic/update_book_mechanic.html'
    success_url = '/'

def update_profile(request):
    user_info = get_object_or_404(User,pk=request.user.pk)
    other_info = get_object_or_404(User_Signup, pk=user_info.user_content.pk)
    user = user_info
    if request.method == "POST":
        username = request.POST['name']
        phone = request.POST["phone"]
        address = request.POST['address']
        mobile = request.POST['mobile']
        email = request.POST['email']

        # User model
        user_info.first_name = username
        user_info.email = email
        # Custom Model
        other_info.phone = phone
        other_info.address = address
        other_info.mobile = mobile

        user_info.save()
        other_info.save()

        return HttpResponseRedirect('/shop/profile/')


    return render(request,'authenticate/update_my_profile.html',context={'user':user,'user_info':user_info,'other_info':other_info})


def ChangePassword(request):
    user = get_object_or_404(User,pk=request.user.pk)
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            messages.error(request,'Password does not matched')
            return redirect('/shop/login/')
        else:
            user.set_password(password)
            user.save()
    return render(request,'authenticate/change_password.html')

def ChangeProfilePhoto(request):
    user0 = get_object_or_404(User,pk=request.user.pk)
    user = get_object_or_404(User_Signup,pk=user0.user_content.pk)
    if request.method == "POST" and request.FILES['profile_image']:
        image = request.FILES['profile_image']
        user.image = image
        user.save()
        return redirect('/shop/profile/')
    return render(request,'authenticate/change_profile_photo.html')


def booknow(request,pk):
    book = get_object_or_404(Product,pk=pk)
    if request.method=="POST":
        items_json = str({'pr'+str(book.id):[1,str(book.product_name),book.price]})
        name = request.POST.get('name', '')
        amount = book.price
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        # return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
        # Request paytm to transfer the amount to your account after payment by user
        param_dict = {

                'MID': 'Your-Merchant-Id-Here',
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})

    return render(request, 'shop/book_now.html',context={'book':book})

