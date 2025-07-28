from django.contrib import admin
from .models import Product, Wishlist,Category,ProductImage,Coupon

# Register your models here.
admin.site.register(Product)
admin.site.register(Wishlist)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(Coupon)
