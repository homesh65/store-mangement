from .forms import StoreForm, AddStoreForm, SaleFrom
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Store, AddStore, Sale
from django.core import serializers
from django.db.models import Count
import datetime

def signupuser(request):
    if(request.method == 'GET'):
        return render(request, 'store/signupuser.html', {'form':UserCreationForm})
    else:
        if( request.POST['password1'] == request.POST['password2'] ):
            try:
                user = User.objects.create_user(request.POST['username'], password = request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'store/signupuser.html', {'form':UserCreationForm , 'error': 'user name already taken'})
        else:
            return render(request, 'store/signupuser.html', {'form':UserCreationForm , 'error': 'password doesn\'t match'})

def loginuser(request):
    if(request.method == 'GET'):
        return render(request, 'store/loginuser.html', {'form':AuthenticationForm})
    else:
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
        if user == None:
            return render(request, 'store/loginuser.html', {'form':AuthenticationForm, 'error':'User doesn\'t exist or username or password doesn\'t match' })
        else:
            login(request, user)
            return redirect('home')

@login_required
def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('loginuser')
    else:
        return redirect('loginuser')
        
@login_required
def home(request):
    addstore = AddStore.objects.all()
    return render(request, 'store/home.html', { 'addstore': addstore })

@login_required
def stock(request):
    store = Store.objects.all()
    store_form = StoreForm()
    addstoreform = AddStoreForm()
    addstore = AddStore.objects.all()
    if request.method == 'GET':
        if request.user.is_superuser:
            return render(request, 'store/stockx.html', {'store_form': store_form, 'addstoreform': addstoreform, 'addstore': addstore, 'error': 'Welcome user', 'store':store} )
        else: 
            return redirect('/home')
    else:
        item = request.POST['item']
        q = float(request.POST['quantityNo'])
        c = float(request.POST['costPrice'])
        s = float(request.POST['sellingPrice'])
        if( q >= 0 and c>=0 and s>=0):
            try:
                temp = AddStore.objects.get(item=item)
                temp.quantityNo = q
                temp.quantityUnit = request.POST['quantityUnit']
                temp.costPrice = c
                temp.sellingPrice = s
                temp.save()
                error = "Stock "+item+" Updated"
            except:
                store = Store.objects.get(item_name=item)
                temp = AddStore.objects.create(item=store , quantityNo=q, costPrice=c, sellingPrice=s, quantityUnit= request.POST['quantityUnit'])
                temp.save()
                error = "Stock "+item+" saved"
            return render(request, 'store/stockx.html', {'store_form': store_form, 'addstoreform': addstoreform, 'addstore': addstore, 'error': error, 'store':store} )
        else:
            error = 'Quantity, CostPrice, SellingPrice must be great than or equal to 0.0'
        addstore = AddStore.objects.all()
        return render(request, 'store/stockx.html', {'store_form': store_form, 'addstoreform': addstoreform, 'addstore': addstore, 'error': 'Welcome user', 'store':store} )


@login_required
def sale(request):
    if request.method == 'GET':
        cdate = datetime.datetime.now().date()
        s = Sale.objects.filter(created_at__date=cdate)
        if(list(s) == []):
            return render(request, 'store/sale.html',{'sale': s, 'temp':True, 'msg':'Today no sales are made yet!'})
        else:
            return render(request, 'store/sale.html',{'sale': s, 'temp':False, 'cdate': cdate})
    else:
        s = Sale.objects.filter(created_at__date=request.POST['cdate'])
        if(list(s) == []):
            if( datetime.datetime.now().date().strftime("%Y-%m-%d") == request.POST['cdate'] ):
                return render(request, 'store/sale.html',{'sale': s, 'temp':True, 'msg':'Today no sales are made yet!'})
            else:
                return render(request, 'store/sale.html',{'sale': s, 'temp':True, 'msg': "No sales made on "+request.POST['cdate']+" day"})
        else:
            return render(request, 'store/sale.html',{'sale': s, 'temp':False, 'cdate':request.POST['cdate']})


@login_required
def item(request):
    if request.method == 'GET':
        return redirect('/home')
    else:
        newItem = request.POST['newItem']
        catagories = request.POST['catagories']
        item = request.POST['item_name']
        if catagories != '':
            if newItem == '':
                store = Store.objects.create(item_name=item, catagories=catagories)
                store.save()
                error = 'New item added sucessfully'
            else:
                store = Store.objects.get(item_name=newItem)
                store.catagories = catagories
                store.save()
                error = 'Item updated sucessfully'
        else:
            error = 'Catagories in Add a new item shouldn\'t be empty'
        store = Store.objects.all()
        store_form = StoreForm()
        addstoreform = AddStoreForm()
        addstore = AddStore.objects.all()
        return render(request, 'store/stockx.html', {'store_form': store_form, 'addstoreform': addstoreform, 'addstore': addstore, 'error': error, 'store':store} )

@login_required
def updatesale(request):
    salefrom = SaleFrom()
    addstore = AddStore.objects.all()  
    if request.method == 'GET':
        return render(request, 'store/updatesale.html', {'salefrom': salefrom, 'addstore': addstore, 'msg':'welcome user'})
    else:
        item = request.POST['item']
        soldquantity = float(request.POST['soldquantity'])
        quantityNo = float(request.POST['quantity'].split(' ')[0])
        if quantityNo == 0:
            return render(request, 'store/updatesale.html', {'salefrom': salefrom, 'addstore': addstore, 'msg':item+' already sold'})
        elif quantityNo-soldquantity >= 0:
            temp = AddStore.objects.get(item=item)
            sale = Sale.objects.create(item= temp, soldquantity=soldquantity) 
            return render(request, 'store/updatesale.html', {'salefrom': salefrom, 'addstore': addstore, 'msg':'Updated sucessfully'})
        else:
            return render(request, 'store/updatesale.html', {'salefrom': salefrom, 'addstore': addstore, 'msg':'Something went wrong'})

       

