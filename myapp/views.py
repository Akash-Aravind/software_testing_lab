from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    return render(request,'index.html')
def products(request):
    return render(request,'products.html')
def cart(request):
    return render(request,'cart.html')
def product_details(request):
    return render(request,'product-details.html')