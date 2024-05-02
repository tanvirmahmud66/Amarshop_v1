from django.contrib import admin
from .models import (
    User,
    Customer,
    Profile,
    Categories,
    SubCategory, 
    Brand, 
    Product,
    Product_Image, 
    Supplier,
    Purchase,
    PurchaseLineUp, 
    ProductLineUp, 
    Sales
)
# Register your models here.

class UserAdminView(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_superuser','is_staff','profile_pic')

class CustomerAdminView(admin.ModelAdmin):
    list_display = ('id','user','name','email','phone','address')

class ProfileAdminview(admin.ModelAdmin):
    list_display = ('id','user','about','phone', 'address')


class CategroyAdminView(admin.ModelAdmin):
    list_display = ('id', 'category')

class SubCategoryAdminView(admin.ModelAdmin):
    list_display = ('id','name','category')

class BrandAdminView(admin.ModelAdmin):
    list_display = ('id','brand')


class ProductAdminView(admin.ModelAdmin):
    list_display = ('id','category','subcategory','brand','product_name','product_code','quantity','stock_alert','cost','price','description','barcode','created_at')

class ProductImageAdminView(admin.ModelAdmin):
    list_display = ('id','product','image')


class SupplierAdminView(admin.ModelAdmin):
    list_display = ('id','company_name', 'contact_person', 'email', 'phone_number','address','created_at')


class PurchaseAdminView(admin.ModelAdmin):
    list_display = ('id','supplier','status','payment_status','grand_total','paid','due','date','total_discount','total_tax','shipping')

class PurchaseLineUpAdminView(admin.ModelAdmin):
    list_display = ('id','author','product','product_name','category','subcategory','brand','unit_price','quantity','subtotal','discount','tax','purchase_confirm','purchase_reference')


class InvoiceAdminView(admin.ModelAdmin):
    list_display = ('id','author','product','quantity','subtotal','sale_confirm','sale_reference')


class SalesAdminView(admin.ModelAdmin):
    list_display = ('id','customer','total_quantity','grand_total','paid','due','status','payment_status','sales_date')


admin.site.register(User, UserAdminView)
admin.site.register(Customer,CustomerAdminView)
admin.site.register(Profile, ProfileAdminview)
admin.site.register(Categories, CategroyAdminView)
admin.site.register(SubCategory, SubCategoryAdminView)
admin.site.register(Brand, BrandAdminView)
admin.site.register(Product,ProductAdminView)
admin.site.register(Product_Image,ProductImageAdminView)
admin.site.register(Supplier, SupplierAdminView)
admin.site.register(Purchase, PurchaseAdminView)
admin.site.register(PurchaseLineUp, PurchaseLineUpAdminView)
admin.site.register(Sales, SalesAdminView)
admin.site.register(ProductLineUp,InvoiceAdminView)