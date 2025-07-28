from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Product, Wishlist, Cart, Category, ProductImage, Coupon


# ---------------------------
# Home
# ---------------------------
def home(request):
    return render(request, "index.html")


# ---------------------------
# Authentication
# ---------------------------
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Wishlist, Cart  # make sure these exist

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Wishlist.objects.create(user=user)
            Cart.objects.create(user=user)
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})



def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")


# ---------------------------
# Products
# ---------------------------
def products(request):
    query = request.GET.get("q", "")
    category_id = request.GET.get("category", "")
    min_price = request.GET.get("min_price", "")
    max_price = request.GET.get("max_price", "")

    product_list = Product.objects.all()

    if query:
        product_list = product_list.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if category_id:
        product_list = product_list.filter(category_id=category_id)
    if min_price:
        product_list = product_list.filter(price__gte=min_price)
    if max_price:
        product_list = product_list.filter(price__lte=max_price)

    categories = Category.objects.all()

    return render(request, "products.html", {
        "products": product_list,
        "categories": categories,
        "query": query
    })


def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    images = product.images.all()  # related_name="images"
    return render(request, "product-details.html", {
        "product": product,
        "images": images
    })


# ---------------------------
# Wishlist
# ---------------------------
@login_required
def wishlist_view(request):
    wishlist = Wishlist.objects.get(user=request.user)
    return render(request, "wishlist.html", {"wishlist": wishlist})


@login_required
def add_to_wishlist(request, product_id):
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    wishlist.products.add(product)
    return redirect("wishlist")


@login_required
def remove_from_wishlist(request, product_id):
    wishlist = Wishlist.objects.get(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    wishlist.products.remove(product)
    return redirect("wishlist")


# ---------------------------
# Cart
# ---------------------------
@login_required
def cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    products = cart.products.all()
    total_price = sum(p.price for p in products)

    # Apply coupon discount
    discount = request.session.get("coupon_discount", 0)
    discount_amount = (total_price * discount) / 100
    final_price = total_price - discount_amount

    return render(request, "cart.html", {
        "cart": cart,
        "total_price": total_price,
        "discount": discount,
        "final_price": final_price,
        "item_count": products.count()
    })


@login_required
def add_to_cart(request, product_id):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart.products.add(product)
    return redirect("cart")


@login_required
def remove_from_cart(request, product_id):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart.products.remove(product)
    return redirect("cart")


# ---------------------------
# Coupon
# ---------------------------
@login_required
def apply_coupon(request):
    if request.method == "POST":
        code = request.POST.get("coupon_code")
        try:
            coupon = Coupon.objects.get(code=code, active=True)
            request.session["coupon_code"] = coupon.code
            request.session["coupon_discount"] = coupon.discount_percentage
        except Coupon.DoesNotExist:
            request.session["coupon_error"] = "Invalid coupon"
    return redirect("cart")
