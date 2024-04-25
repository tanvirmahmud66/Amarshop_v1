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
    Inventory, 
    Supplier,
    Transaction,
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
    list_display = ('id','category','subcategory','brand','product_name','product_code','cost','price','description','productImg','created_at')

class ProductImageAdminView(admin.ModelAdmin):
    list_display = ('id','product','image')

class InventoryAdminView(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity','stock_alert','unit_price','unit_cost','total_cost','valuation','profit','last_updated', 'created_at')


class SupplierAdminView(admin.ModelAdmin):
    list_display = ('id','company_name', 'contact_person', 'email', 'phone_number','address','created_at')


class TransactionAdminView(admin.ModelAdmin):
    list_display = ('id','product','sale','transaction_type','payment_method','amount','reference', 'transaction_date')


class PurchaseAdminView(admin.ModelAdmin):
    list_display = ('id','supplier','status','payment_status','grand_total','paid','due','date','total_discount','total_tax','shipping')

class PurchaseLineUpAdminView(admin.ModelAdmin):
    list_display = ('id','product','product_name','category','subcategory','brand','unit_price','quantity','subtotal','discount','tax','purchase_confirm','purchase_reference')


class InvoiceAdminView(admin.ModelAdmin):
    list_display = ('id','token','sale_reference','product','quantity','subtotal','sale_confirm')


class SalesAdminView(admin.ModelAdmin):
    list_display = ('id','customer','amount','product_quantity','sales_date')


admin.site.register(User, UserAdminView)
admin.site.register(Customer,CustomerAdminView)
admin.site.register(Profile, ProfileAdminview)
admin.site.register(Categories, CategroyAdminView)
admin.site.register(SubCategory, SubCategoryAdminView)
admin.site.register(Brand, BrandAdminView)
admin.site.register(Product,ProductAdminView)
admin.site.register(Product_Image,ProductImageAdminView)
admin.site.register(Inventory, InventoryAdminView)
admin.site.register(Supplier, SupplierAdminView)
admin.site.register(Transaction,TransactionAdminView)
admin.site.register(Purchase, PurchaseAdminView)
admin.site.register(PurchaseLineUp, PurchaseLineUpAdminView)
admin.site.register(ProductLineUp,InvoiceAdminView)
admin.site.register(Sales, SalesAdminView)