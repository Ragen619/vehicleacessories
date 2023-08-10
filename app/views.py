from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from.forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



class ProductView(View):
    def get(self,request):
        cardecoration = Product.objects.filter(category='C')
        volkswagen = Product.objects.filter(category='V')
        toyota = Product.objects.filter(category='T')
        return render(request, 'app/home.html',{'cardecoration':cardecoration,'volkswagen':volkswagen,'toyota':toyota})



class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html', {'product':product})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        # print(cart)
        amount = 0.0
        shipping_amount = 50.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount= amount + shipping_amount
            return render(request, 'app/addtocart.html', {'carts':cart, 'totalamount':totalamount, 'amount':amount})
        else:
            return render(request,'app/emptycart.html')


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount= 0.0
        shipping_amount= 50.0
        cart_product = [p for p in Cart.objects.all() if p.user ==request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount


        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount':amount + shipping_amount
            }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount= 0.0
        shipping_amount= 50.0
        cart_product = [p for p in Cart.objects.all() if p.user ==request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount


        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount':amount + shipping_amount
            }
        return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount= 0.0
        shipping_amount= 50.0
        cart_product = [p for p in Cart.objects.all() if p.user ==request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'amount': amount,
            'totalamount':amount + shipping_amount
            }
        return JsonResponse(data)






@login_required
def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-dark'})

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op})


 
def cardecoration(request , data=None):
    if data==None:
        cardecoration = Product.objects.filter(category='C')
    elif data =='Volkswagen' or data=='Toyota':
        cardecoration=Product.objects.filter(category='C').filter(brand=data)
    elif data== 'below':
        cardecoration=Product.objects.filter(category='C').filter(discounted_price__lt=10000)
    elif data== 'above':
        cardecoration=Product.objects.filter(category='C').filter(discounted_price__gt=10000)

    return render(request, 'app/cardecoration.html', {'cardecoration':cardecoration})

def cars_serviceparts(request , data=None):
    if data==None:
        cars_serviceparts = Product.objects.filter(category='CS')
    elif data =='Battery' or data=='Brakes':
        cars_serviceparts=Product.objects.filter(category='CS').filter(brand=data)
    elif data== 'below':
        cars_serviceparts=Product.objects.filter(category='CS').filter(discounted_price__lt=10000)
    elif data== 'above':
        cars_serviceparts=Product.objects.filter(category='CS').filter(discounted_price__gt=10000)

    return render(request, 'app/cars_serviceparts.html', {'cars_serviceparts':cars_serviceparts})

def modifications(request , data=None):
    if data==None:
        modifications = Product.objects.filter(category='M')
    elif data =='Brembo' or data=='Motul':
        modifications=Product.objects.filter(category='M').filter(brand=data)
    elif data== 'below':
        modifications=Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    elif data== 'above':
        modifications=Product.objects.filter(category='M').filter(discounted_price__gt=10000)

    return render(request, 'app/modifications.html', {'modifications':modifications})


def bikes_serviceparts(request , data=None):
    if data==None:
        bikes_serviceparts = Product.objects.filter(category='BS')
    elif data =='RCB' or data=='WP':
        bikes_serviceparts=Product.objects.filter(category='BS').filter(brand=data)
    elif data== 'below':
        bikes_serviceparts=Product.objects.filter(category='BS').filter(discounted_price__lt=10000)
    elif data== 'above':
        bikes_serviceparts=Product.objects.filter(category='BS').filter(discounted_price__gt=10000)

    return render(request, 'app/bikes_serviceparts.html', {'bikes_serviceparts':bikes_serviceparts})


class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})

    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congrats!! You have been registered successfully')
            form.save()
        return render(request,'app/customerregistration.html',{'form':form})

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 50.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user ==request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount
    return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items})

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

@method_decorator(login_required,name='dispatch')

class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-dark'})
    
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg= Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Congrats!! Profile has been updated')
        return render(request,'app/profile.html',{'form':form,'active':'btn-dark'})
