from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Product, Wishlist

def home(request):
    return render(request, 'index.html')

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart.html', {'cart': cart})



def products(request):
    all_products = Product.objects.all()
    return render(request, 'products.html', {'products': all_products})

def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product-details.html', {'product': product})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Wishlist.objects.create(user=user)  # Create wishlist for new user
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def wishlist_view(request):
    wishlist = Wishlist.objects.get(user=request.user)
    return render(request, 'wishlist.html', {'wishlist': wishlist})

@login_required
def add_to_wishlist(request, product_id):
    wishlist = Wishlist.objects.get(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    wishlist.products.add(product)
    return redirect('wishlist')

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Cart, Product

@login_required
def add_to_cart(request, product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart.products.add(product)
    return redirect('cart')

@login_required
def remove_from_cart(request, product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart.products.remove(product)
    return redirect('cart')



@login_required
def remove_from_wishlist(request, product_id):
    wishlist = Wishlist.objects.get(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    wishlist.products.remove(product)
    return redirect('wishlist')
