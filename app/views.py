from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import AccessMixin
from datetime import datetime
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.utils import timezone
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import DeleteView
from django.db.models import Q
from django.db.models import Sum
from django.db.models.functions import ExtractWeekDay
from django.views.generic import (
    TemplateView, 
    ListView, 
    CreateView, 
    DetailView, 
    UpdateView
)
from .models import (
    User,
    Categories, 
    Brand, 
    Inventory, 
    Product, 
    Supplier,
    Purchase,
    Transaction,
    GeneralUser, 
    ProductLineUp,
    Sales
)
from .forms import (
    AdminCreateForm,
    UserProfilePictureForm,
    ProfileUpdateForm,
    CategoryForm , 
    BrandForm, 
    InventoryForm,
    InventoryPriceSetForm,
    Productform, 
    SupplierForm,
    PurchaseForm,
    GeneralUserForm,
    ProductLineUpForm,
    TransactionForm,
    SalesForm
)

# =========================================AUTHENTICATION SECTION===================================
# ---------------------------------------------------- Mixin
class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class PreventLoggedInMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
    
# -------------------------------------------------Admin singup view
class AdminCreateView(PreventLoggedInMixin,CreateView):
    template_name = 'authentication/singup.html'
    form_class = AdminCreateForm
    success_url = reverse_lazy('dashboard')


# -------------------------------------------------Admin login view
class AdminLoginView(PreventLoggedInMixin,LoginView):
    template_name = 'authentication/login.html'
    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy('dashboard')
        else:
            print("User is not staff")
            return reverse_lazy('admin-login')


# ----------------------------------------------------------Admin logout view
class AdminLogoutView(SuperuserRequiredMixin, LogoutView):
    next_page = reverse_lazy('admin-login')




# ========================================= Admin User profile =====================================
# ---------------------------------------------------------- Profile view
class ProfileView(SuperuserRequiredMixin, DetailView):
    model = User
    context_object_name = 'profile'
    template_name = 'profile/profile.html'

    def get_object(self, queryset=None):
        pk = self.request.user.id
        return self.model.objects.get(id=pk)


# ---------------------------------------------------------- Profile change picture View
class ProfilePictureChangeView(SuperuserRequiredMixin,UpdateView):
    model = User
    form_class = UserProfilePictureForm
    template_name = 'profile/pictureChange.html'

    def get_success_url(self):
        return reverse('profile',kwargs={'pk': self.kwargs.get('pk', None)})


# ---------------------------------------------------------- Profile Picture Remove View
class ProfilePictureRemoveView(UpdateView):
    model = User
    form_class = UserProfilePictureForm
    context_object_name = 'profile'
    template_name = 'profile/pictureRemove.html'

    def get_success_url(self):
        return reverse('profile',kwargs={'pk': self.kwargs.get('pk', None)})

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.profile_pic = None
        obj.save
        return super().form_valid(form)


# ---------------------------------------------------------- Profile Update View
class ProfileUpdateView(SuperuserRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'profile/profileUpdate.html'

    def get_success_url(self):
        return reverse('profile',kwargs={'pk': self.kwargs.get('pk', None)})



# =========================================DASHBOARD SECTION========================================
class DashboardView(SuperuserRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sales_data = Sales.objects.all()
        purchase_data = Purchase.objects.all()
        stock_alert_data = Inventory.objects.filter(quantity__lt=5)
        category_data = Categories.objects.all()
        brand_data = Brand.objects.all()
        sales = 0
        purchase = 0
        debt = 0
        top_sale = []
        top_brand = []
        for each in sales_data:
            sales += each.amount
        for each in purchase_data:
            purchase += each.paid_ammount
            debt += each.due_amount
        for each in category_data:
            product_types = ProductLineUp.objects.filter(product__product__category=each, sale_confirm=True)
            product_count = 0
            for each_item in product_types:
                product_count += each_item.quantity
            top_sale.append({
                f"{each}": product_count
            })
        for each in brand_data:
            product_types = ProductLineUp.objects.filter(product__product__brand=each, sale_confirm=True)
            brand_count = 0
            for each_item in product_types:
                brand_count += each_item.quantity
            top_brand.append({
                f"{each}": brand_count
            })
        
        current_year = timezone.now().year
        current_month = timezone.now().month
        monthly_sales_data = Sales.objects.filter(sales_date__year=current_year, sales_date__month=current_month)

        context['sales'] = sales
        context['purchase'] = purchase
        context['debt'] = debt
        context['stock_alert'] = stock_alert_data
        context['top_sale'] = sorted(top_sale, key=lambda x: list(x.values())[0], reverse=True)[:5]
        context['top_brand'] = sorted(top_brand, key=lambda x: list(x.values())[0], reverse=True)[:5]
        context['monthly_sales'] = monthly_sales_data
        return context




# ==========================================SALES SECTION=======================================

# --------------------------------------------------------------- Sales List View
class SalesListView(SuperuserRequiredMixin, ListView):
    model = Sales
    context_object_name = 'Sales'
    template_name = 'inventory/sales/salesList.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_q = self.request.GET.get('q', None)

        # if search_q:
        #     queryset = queryset.filter(user__first_name__icontains=search_q)
            
        if search_q:
            queryset = queryset.filter(
                Q(general_user__first_name__icontains=search_q) |
                Q(general_user__last_name__icontains=search_q) |
                Q(general_user__email__icontains=search_q) | 
                Q(user__first_name__icontains=search_q) |
                Q(user__last_name__icontains=search_q) |
                Q(user__email__icontains=search_q) 
            )

        return queryset

# --------------------------------------------------------------- Sale Details View
class SaleDetailsView(SuperuserRequiredMixin, DetailView):
    model = Sales
    context_object_name = "sale"
    template_name = 'inventory/sales/saleDetails.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sale_instance = self.object
        product_list = ProductLineUp.objects.filter(sale_reference=sale_instance)
        grand_total = product_list.aggregate(total_amount=Sum('subtotal'))['total_amount']
        context['invoice_list'] = product_list
        context['grand_total'] = grand_total
        if sale_instance.user:
            transaction = Transaction.objects.filter(sale=sale_instance).first()
        else:
            transaction = Transaction.objects.filter(sale=sale_instance).first()
        context['transaction'] = transaction
        return context


# --------------------------------------------------------------- General user create view
class ClientUserView(SuperuserRequiredMixin, CreateView):
    model = GeneralUser
    form_class = GeneralUserForm
    template_name = 'inventory/sales/createClientUser.html'

    def get_success_url(self):
        return reverse('invoice-list',kwargs={'pk': self.object.email})
    
    def form_valid(self, form):
        self.first_name = form.cleaned_data['first_name']
        self.last_name = form.cleaned_data['last_name']
        self.email = form.cleaned_data['email']
        self.phone = form.cleaned_data['phone']

        if self.email:
            user = User.objects.filter(email=self.email).first()
            if user:
                return redirect('invoice-list', pk=self.email)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        email = form.data['email']
        general_user = GeneralUser.objects.filter(email=email).first()
        if general_user:
            return redirect('invoice-list', pk=form.data['email'])
        return super().form_invalid(form)
    

   
# --------------------------------------------------------------- invoice list
class InvoiceListView(SuperuserRequiredMixin, ListView):
    model = ProductLineUp
    template_name = 'inventory/sales/invoiceList.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_list = ProductLineUp.objects.filter(token = self.kwargs.get('pk'), sale_confirm=False)
        context['product_list'] = product_list
        total_amount = product_list.aggregate(total_amount=Sum('subtotal'))['total_amount']
        total_quantity = product_list.aggregate(total_quantity=Sum('quantity'))['total_quantity']
        context['total_amount'] = total_amount
        context['total_quantity'] = total_quantity
        pk = self.kwargs.get('pk')
        print(pk)
        if pk:
            if User.objects.filter(email=pk).exists():
                context['buyer'] = User.objects.filter(email=pk).first()
            if GeneralUser.objects.filter(email=pk).exists():
                context['buyer'] = GeneralUser.objects.filter(email=pk).first()
        return context


# ---------------------------------------------------------------- invoice add item
class InvoiceAddItem(SuperuserRequiredMixin, CreateView):
    model = ProductLineUp
    form_class = ProductLineUpForm
    template_name = 'inventory/sales/invoiceAddItem.html'

    def get_success_url(self):
        return reverse('invoice-list',kwargs={'pk': self.kwargs.get('pk', None)})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = self.kwargs.get('pk',None)
        return context
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        token_param = self.kwargs.get('pk', None)
        obj.token = token_param
        obj.subtotal = obj.quantity * obj.product.unit_price
        obj.save()
        return super().form_valid(form)
    

def get_filtered_products(request):
    category_id = request.GET.get('category_id')
    brand_id = request.GET.get('brand_id')
    category = Categories.objects.get(id=category_id)
    brand = Brand.objects.get(id=brand_id)
    print(category_id, brand_id)
    products = Inventory.objects.filter(product__category=category, product__brand=brand).values('id','product__model')
    print(products)
    return JsonResponse({'products': list(products)})


#----------------------------------------------------------------- invoice remove item
class InvoiceRemoveItem(SuperuserRequiredMixin, DeleteView):
    model = ProductLineUp
    context_object_name = 'invoiceItem'
    template_name = 'inventory/sales/invoiceRemoveItem.html'

    def get_success_url(self):
        return reverse('invoice-list',kwargs={'pk': self.kwargs.get('email', None)})   


# --------------------------------------------------------------- Sales payment
class SalesPayment(SuperuserRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'inventory/sales/salesPayment.html'

    def get_success_url(self):
        return reverse('sales-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = self.kwargs.get('pk', None)
        product_list = ProductLineUp.objects.filter(token = self.kwargs.get('pk'), sale_confirm=False)
        context['product_list'] = product_list
        total_amount = product_list.aggregate(total_amount=Sum('subtotal'))['total_amount']
        total_quantity = product_list.aggregate(total_quantity=Sum('quantity'))['total_quantity']
        context['total_amount'] = total_amount
        context['total_quantity'] = total_quantity
        pk = self.kwargs.get('pk')
        if pk:
            if User.objects.filter(email=pk).exists():
                context['customer'] = User.objects.filter(email=pk).first()
            if GeneralUser.objects.filter(email=pk).exists():
                context['customer'] = GeneralUser.objects.filter(email=pk).first()
        return context
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        email = self.kwargs.get('pk',None)
        obj.transaction_type = "IN"
        obj.reference = email
        obj.transaction_date = datetime.now()
        invoice_list = ProductLineUp.objects.filter(token=email, sale_confirm=False)
        self.total_product=0
        for each in invoice_list:
            self.total_product += each.quantity
            each.sale_confirm = True
            inventory = Inventory.objects.get(product=each.product.product)
            inventory.quantity -= each.quantity
            inventory.save()
            each.save()
        user = User.objects.filter(email=email).first()
        if user:
            self.sale = Sales.objects.create(
                user=user,
                amount=obj.amount,
                product_quantity=self.total_product,
                sales_date = obj.transaction_date
            )
            self.sale.save()
            obj.sale = self.sale
            obj.save()
        else:
            general_user = GeneralUser.objects.get(email=email)
            self.sale = Sales.objects.create(
                general_user=general_user,
                amount=obj.amount,
                product_quantity=self.total_product,
                sales_date = obj.transaction_date
            )
            self.sale.save()
            obj.sale = self.sale
            obj.save()
        for each in invoice_list:
            each.sale_reference = self.sale
            each.save()
        return super().form_valid(form)



# ==========================================INVENTORY SECTION=======================================
# ---------------------------------------------------------------Inventory list view
class InventoryListView(SuperuserRequiredMixin,ListView):
    model = Inventory
    context_object_name = 'inventories'
    template_name = 'inventory/inventoryList.html'
    categories_model = Categories.objects.all()
    brand_model = Brand.objects.all()
    extra_context = {
        'categories': categories_model,
        'brands': brand_model
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', None)
        cate = self.request.GET.get('category', None)
        brand = self.request.GET.get('brand',None)
        price = self.request.GET.get('price',None)
        if search_query:
            queryset = queryset.filter(product__model__icontains=search_query)

        if cate:
            queryset = queryset.filter(product__category__id=cate)
        if brand:
            queryset = queryset.filter(product__brand__id=brand)
        if price:
            queryset = queryset.filter(product__price__gte=price)

        if brand and cate and price==None:
            queryset = queryset.filter(
                 Q(product__brand__id=brand) &
                 Q(product__category__id=cate)
            )
        elif price and cate and brand==None:
            queryset = queryset.filter(
                 Q(product__price__gte=price) &
                 Q(product__category__id=cate)
            )
        elif price and brand and cate==None:
            queryset = queryset.filter(
                 Q(product__price__gte=price) &
                 Q(product__brand__id=brand)
            )
        elif price and brand and cate:
            queryset = queryset.filter(
                 Q(product__price__gte=price) &
                 Q(product__brand__id=brand) &
                 Q(product__category__id=cate)
            )

        return queryset
    


## ---------------------------------------------------------------Inventory detail view
class InventoryDetailsView(SuperuserRequiredMixin,DetailView):
    model = Inventory
    template_name = 'inventory/inventoryDetails.html'
    context_object_name = 'inventory'


#---------------------------------------------------------------- Inventory Priduct price set
class InventoryPriceSet(SuperuserRequiredMixin,UpdateView):
    model = Inventory
    form_class = InventoryPriceSetForm
    context_object_name = 'inventory'
    template_name = 'inventory/inventorySetPrice.html'
    success_url = reverse_lazy('inventory-list')

    def form_valid(self, form):
        self.unit_price = form.cleaned_data['unit_price']
        product = Product.objects.get(id=self.object.product.id)
        if product:
            product.price = self.unit_price
            product.save()
        return super().form_valid(form)


# ---------------------------------------------------------------Inventory Update view
class InventoryUpdateView(SuperuserRequiredMixin,UpdateView):
    model = Inventory
    form_class = InventoryForm
    context_object_name = 'inventory'
    template_name = 'inventory/inventoryUpdate.html'

    def get_success_url(self):
        return reverse('inventory-details',kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        self.unit_price = form.cleaned_data['unit_price']
        self.unit_cost = form.cleaned_data['unit_cost']
        product = Product.objects.get(id=self.object.product.id)
        if product:
            product.cost = self.unit_cost
            product.price = self.unit_price
            product.save()
        return super().form_valid(form)



# ---------------------------------------------------------------Inventory delete view
class InventoryDeleteView(SuperuserRequiredMixin,DeleteView):
    model = Inventory
    template_name = 'inventory/inventoryDelete.html'
    context_object_name = 'inventory'
    success_url = reverse_lazy('inventory-list')



# ==========================================PURCHASE SECTION=======================================
#----------------------------------------------------------------Purchase list view
class PurchaseListView(SuperuserRequiredMixin,ListView):
    model = Purchase
    context_object_name = 'purchases'
    template_name = 'inventory/purchase/purchaseList.html'
    categories = Categories.objects.all()
    brand = Brand.objects.all()
    supplier = Supplier.objects.all()
    extra_context = {
        'categories': categories,
        'brands': brand,
        'suppliers': supplier,
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', None)
        category = self.request.GET.get('category', None)
        brand = self.request.GET.get('brand',None)
        supplier = self.request.GET.get('supplier',None)
        purchase_date = self.request.GET.get('purchase_date',None)

        if search_query:
            queryset = queryset.filter(model__icontains=search_query)

        if category:
            queryset = queryset.filter(category=category)
        if brand:
            queryset = queryset.filter(brand=brand)
        if supplier:
            queryset = queryset.filter(supplier=supplier)
        if purchase_date:
            date_object = datetime.strptime(purchase_date, "%Y-%m-%d").date()
            queryset = queryset.filter(Q(purchase_date__date=date_object))

        if category and brand and supplier==None and purchase_date==None:
            queryset = queryset.filter(
                Q(category=category) &
                Q(brand=brand)
            )
        elif category and brand==None and supplier and purchase_date==None:
            queryset = queryset.filter(
                Q(category=category) &
                Q(supplier=supplier)
            )
        elif category and brand==None and supplier==None and purchase_date:
            date_object = datetime.strptime(purchase_date, "%Y-%m-%d").date()
            queryset = queryset.filter(
                Q(category=category) &
                Q(purchase_date__date=date_object)
            )
        elif category==None and brand and supplier and purchase_date==None:
            queryset = queryset.filter(
                Q(brand=brand) &
                Q(supplier=supplier)
            )
        elif category==None and brand and supplier==None and purchase_date:
            date_object = datetime.strptime(purchase_date, "%Y-%m-%d").date()
            queryset = queryset.filter(
                Q(brand=brand) &
                Q(purchase_date__date=date_object)
            )
        elif category==None and brand==None and supplier and purchase_date:
            date_object = datetime.strptime(purchase_date, "%Y-%m-%d").date()
            queryset = queryset.filter(
                Q(supplier=supplier) &
                Q(purchase_date__date=date_object)
            )
        elif category and brand and supplier and purchase_date==None:
            queryset = queryset.filter(
                Q(category=category) &
                Q(brand=brand) &
                Q(supplier=supplier)
            )
        elif category and brand and supplier==None and purchase_date:
            date_object = datetime.strptime(purchase_date, "%Y-%m-%d").date()
            queryset = queryset.filter(
                Q(category=category) &
                Q(brand=brand) &
                Q(purchase_date__date=date_object)
            )
        elif category and brand==None and supplier and purchase_date:
            date_object = datetime.strptime(purchase_date, "%Y-%m-%d").date()
            queryset = queryset.filter(
                Q(category=category) &
                Q(supplier=supplier) &
                Q(purchase_date__date=date_object)
            )
        elif category==None and brand and supplier and purchase_date:
            date_object = datetime.strptime(purchase_date, "%Y-%m-%d").date()
            queryset = queryset.filter(
                Q(brand=brand) &
                Q(supplier=supplier) &
                Q(purchase_date__date=date_object)
            )
        elif category and brand and supplier and purchase_date:
            date_object = datetime.strptime(purchase_date, "%Y-%m-%d").date()
            queryset = queryset.filter(
                Q(category=category) &
                Q(brand=brand) &
                Q(supplier=supplier) &
                Q(purchase_date__date=date_object)
            )

        return queryset


# --------------------------------------------------------------- new Purchase view
class PurchaseCreateView(SuperuserRequiredMixin,CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'inventory/purchase/newPurchase.html'
    success_url = reverse_lazy('purchase-list')

    def form_valid(self, form):
        category = form.cleaned_data['category']
        brand = form.cleaned_data['brand']
        model = form.cleaned_data['model']
        quantity = form.cleaned_data['quantity']
        unit_cost = form.cleaned_data['unit_cost']
        payment_method = form.cleaned_data['payment_method']
        paid_ammount = form.cleaned_data['paid_ammount']
        reference = form.cleaned_data['reference']

        if not Product.objects.filter(category=category, brand=brand, model=model).exists():
            self.new_product = Product.objects.create(category=category, brand=brand, model=model, cost=unit_cost)
            self.new_product.save()
        else:
            self.new_product = Product.objects.get(category=category, brand=brand, model=model)

        if Inventory.objects.filter(product=self.new_product).exists():
            self.get_inventory = Inventory.objects.get(product=self.new_product)
            self.get_inventory.quantity += quantity
            self.get_inventory.save()
        else:
            self.new_inventory = Inventory.objects.create(
                product=self.new_product,
                quantity=quantity,
                unit_cost=unit_cost,
            )
            self.new_inventory.save()
        
        self.object = form.save()

        self.new_transaction = Transaction.objects.create(
            product=self.new_product,
            transaction_type = "OUT",
            payment_method=payment_method,
            amount = paid_ammount,
            reference = reference,
            transaction_date = self.object.purchase_date
        )        
        return super().form_valid(form)


# --------------------------------------------------------------- Purchase details view
class PurchaseDetailsView(SuperuserRequiredMixin,DetailView):
    model = Purchase
    context_object_name = 'purchase'
    template_name = 'inventory/purchase/purchaseDetails.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchase = self.get_object()
        supplier = purchase.supplier
        context['supplier'] = supplier
        return context


# --------------------------------------------------------------- Purchase details view
class PurchaseUpdateView(SuperuserRequiredMixin,UpdateView):
    model = Purchase
    form_class = PurchaseForm
    context_object_name = 'purchase'
    template_name = 'inventory/purchase/purchaseUpdate.html'

    def get_success_url(self):
        return reverse('purchase-details',kwargs={'pk': self.object.pk})
    


# --------------------------------------------------------------- Purchase details view
class PurchaseDeleteView(SuperuserRequiredMixin,DeleteView):
    model = Purchase
    context_object_name = 'purchase'
    template_name = 'inventory/purchase/purchaseDelete.html'
    success_url = reverse_lazy('purchase-list')



# ==========================================PRODUCT SECTION=======================================
# ---------------------------------------------------------------product list View
class ProductListView(SuperuserRequiredMixin,ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'inventory/product/productList.html'
    categories_model = Categories.objects.all()
    brand_model = Brand.objects.all()
    extra_context = {
        'categories': categories_model,
        'brands': brand_model
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', None)
        cate = self.request.GET.get('category', None)
        brand = self.request.GET.get('brand',None)
        price = self.request.GET.get('price',None)
        if search_query:
            queryset = queryset.filter(model__icontains=search_query)

        if cate:
            queryset = queryset.filter(category__id=cate)
        if brand:
            queryset = queryset.filter(brand__id=brand)
        if price:
            queryset = queryset.filter(price__gte=price)

        if brand and cate and price==None:
            queryset = queryset.filter(
                 Q(brand__id=brand) &
                 Q(category__id=cate)
            )
        elif price and cate and brand==None:
            queryset = queryset.filter(
                 Q(price__gte=price) &
                 Q(category__id=cate)
            )
        elif price and brand and cate==None:
            queryset = queryset.filter(
                 Q(price__gte=price) &
                 Q(brand__id=brand)
            )
        elif price and brand and cate:
            queryset = queryset.filter(
                 Q(price__gte=price) &
                 Q(brand__id=brand) &
                 Q(category__id=cate)
            )
            
        return queryset


# ---------------------------------------------------------------Product create view
class CreateProductView(SuperuserRequiredMixin,CreateView):
    model = Product
    form_class = Productform
    template_name = 'inventory/product/addProduct.html'

    def get_success_url(self):
        return reverse('product-list')
    
# ---------------------------------------------------------------Product Details view
class ProductDetailsView(SuperuserRequiredMixin,DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'inventory/product/productDetails.html'

# ---------------------------------------------------------------Product update view
class ProductUpdateView(SuperuserRequiredMixin,UpdateView):
    model = Product
    form_class = Productform
    context_object_name = 'product'
    template_name = 'inventory/product/productUpdate.html'

    def get_success_url(self):
        return reverse('product-details',kwargs={'pk': self.object.pk})


# ---------------------------------------------------------------Product Delete View
class ProductDeleteView(SuperuserRequiredMixin,DeleteView):
    model = Product
    context_object_name = 'product'
    template_name = 'inventory/product/productDelete.html'
    success_url = reverse_lazy('product-list')



# ==========================================CATEGORY SECTION=======================================
# ---------------------------------------------------------------Category Create view
class CreateCategoryView(SuperuserRequiredMixin,CreateView):
    model = Categories
    form_class = CategoryForm
    template_name = 'inventory/category/addCategory.html'

    def get_success_url(self):
        return reverse('category-list')


# ---------------------------------------------------------------Categroy list view
class CategoryListView(SuperuserRequiredMixin,ListView):
    model = Categories
    context_object_name = 'categories'
    template_name = 'inventory/category/allcategory.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', None)
        if search_query:
            queryset = queryset.filter(category__icontains=search_query)
        return queryset


# ---------------------------------------------------------------Category Update view
class CategoryUpdateView(SuperuserRequiredMixin,UpdateView):
    model = Categories
    form_class = CategoryForm
    context_object_name = 'category'
    template_name = 'inventory/category/categoryUpdate.html'
    success_url = reverse_lazy('category-list')


# ---------------------------------------------------------------Category Delete view
class CategoryDeleteView(SuperuserRequiredMixin,DeleteView):
    model = Categories
    context_object_name = 'category'
    template_name = 'inventory/category/categoryDelete.html'
    success_url = reverse_lazy('category-list')



# ==========================================BRAND SECTION=======================================
# ---------------------------------------------------------------Brand list view
class BrandListView(SuperuserRequiredMixin,ListView):
    model = Brand
    context_object_name = 'brands'
    template_name = 'inventory/brand/brandList.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', None)
        if search_query:
            queryset = queryset.filter(brand__icontains=search_query)
        return queryset


# ---------------------------------------------------------------Brand create view
class CreateBrandView(SuperuserRequiredMixin,CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'inventory/brand/addbrand.html'

    def get_success_url(self):
        return reverse('brand-list')


# ---------------------------------------------------------------Brand update view
class BrandUpdateView(SuperuserRequiredMixin,UpdateView):
    model = Brand
    form_class = BrandForm
    context_object_name = 'brand'
    template_name = 'inventory/brand/brandUpdate.html'
    success_url = reverse_lazy('brand-list')


# ---------------------------------------------------------------Brand Delete view
class BrandDeleteView(SuperuserRequiredMixin,DeleteView):
    model = Brand
    context_object_name = 'brand'
    template_name = 'inventory/brand/brandDelete.html'
    success_url = reverse_lazy('brand-list')





# ==========================================REPORT SECTION=======================================
class ReportView(SuperuserRequiredMixin,TemplateView):
    template_name = 'reports/report.html'



# ==========================================SUPPLIERS SECTION=======================================
# ---------------------------------------------------------------Supplier List view
class SuppliersListView(SuperuserRequiredMixin,ListView):
    model = Supplier
    context_object_name = 'suppliers'
    template_name = 'suppliers/supplierList.html'

# ---------------------------------------------------------------Supplier create view
class SupplierCreateView(SuperuserRequiredMixin,CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/supplierCreate.html'
    success_url = reverse_lazy('supplier-list')

# ---------------------------------------------------------------Supplier update view
class SupplierUpdateView(SuperuserRequiredMixin,UpdateView):
    model = Supplier
    form_class = SupplierForm
    context_object_name = 'supplier'
    template_name = 'suppliers/supplierUpdate.html'
    success_url = reverse_lazy('supplier-list')

# ---------------------------------------------------------------Supplier delete view
class SupplierDeleteView(SuperuserRequiredMixin,DeleteView):
    model = Supplier
    form_class = SupplierForm
    context_object_name = 'supplier'
    template_name = 'suppliers/supplierDelete.html'
    success_url = reverse_lazy('supplier-list')



# ==========================================ORDER SECTION=======================================
class OrderView(SuperuserRequiredMixin,TemplateView):
    template_name = 'orders/order.html'


# ==========================================MANAGE STORE SECTION=======================================
class StoreManageView(SuperuserRequiredMixin,TemplateView):
    template_name = 'manage/index.html'