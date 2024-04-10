from django.contrib import admin
from .models import (
    User,
    Categories, 
    Brand, 
    Product, 
    Inventory, 
    Supplier,
    Transaction,
    Purchase, 
    GeneralUser, 
    ProductLineUp, 
    Sales
)
# Register your models here.

class UserAdminView(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff','profile_pic')

class CategroyAdminView(admin.ModelAdmin):
    list_display = ('id', 'category')


class BrandAdminView(admin.ModelAdmin):
    list_display = ('id','brand')


class ProductAdminView(admin.ModelAdmin):
    list_display = ('id','category','brand','model','cost','price','description','productImg','released_year','created_at')


class InventoryAdminView(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity','unit_price','unit_cost','total_cost','valuation','profit','last_updated', 'created_at')


class SupplierAdminView(admin.ModelAdmin):
    list_display = ('id','company_name', 'contact_person', 'email', 'phone_number','address','created_at')


class TransactionAdminView(admin.ModelAdmin):
    list_display = ('id','product','sale','transaction_type','payment_method','amount','reference', 'transaction_date')


class PurchaseAdminView(admin.ModelAdmin):
    list_display = ('id','category','brand','model','quantity','unit_cost','supplier','transaction_type','payment_method','paid_ammount','reference','due_amount','purchase_date')


class GeneralUserAdminView(admin.ModelAdmin):
    list_display = ('id','first_name','last_name','email','phone')


class InvoiceAdminView(admin.ModelAdmin):
    list_display = ('id','token','sale_reference','product','quantity','subtotal','sale_confirm')


class SalesAdminView(admin.ModelAdmin):
    list_display = ('id','user','general_user','amount','product_quantity','sales_date')


admin.site.register(User, UserAdminView)
admin.site.register(Categories, CategroyAdminView)
admin.site.register(Brand, BrandAdminView)
admin.site.register(Product,ProductAdminView)
admin.site.register(Inventory, InventoryAdminView)
admin.site.register(Supplier, SupplierAdminView)
admin.site.register(Transaction,TransactionAdminView)
admin.site.register(Purchase, PurchaseAdminView)
admin.site.register(GeneralUser, GeneralUserAdminView)
admin.site.register(ProductLineUp,InvoiceAdminView)
admin.site.register(Sales, SalesAdminView)