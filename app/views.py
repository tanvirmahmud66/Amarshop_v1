from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import AccessMixin
from datetime import datetime
import random
from django.db.models import Count
from django.shortcuts import render
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.utils import timezone
from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import DeleteView
from django.db.models import Q
from django.db.models import Sum
from django.views.generic.edit import FormMixin
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
    Customer,
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
from .forms import (
    AdminCreateForm,
    UserProfilePictureForm,
    ProfileForm,
    CategoryForm,
    SubCategoryForm,
    BrandForm,
    Productform,
    ProductImageForm,
    SupplierForm,
    PurchaseForm,
    PurchaseLinuUpForm,
    CustomerForm,
    ProductLineUpForm,
    PurchaseLineUpform2,
    SalesForm,

)

# =========================================AUTHENTICATION SECTION===================================
# ---------------------------------------------------- Mixin
class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_superuser:
            return self.request.user.is_superuser
        if self.request.user.is_staff:
            return self.request.user.is_staff

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
        if self.request.user.is_staff:
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
    form_class = ProfileForm
    template_name = 'profile/profileUpdate.html'

    def get_success_url(self):
        return reverse('profile',kwargs={'pk': self.kwargs.get('pk', None)})



# =========================================DASHBOARD SECTION========================================
class DashboardView(SuperuserRequiredMixin, TemplateView):
    template_name = 'inventory/dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        sales_data = Sales.objects.all()
        purchase_data = Purchase.objects.all()
        products = Product.objects.all()
        purchases = Purchase.objects.all()

        # -----------Sales, Purchase , Debt, Expenses count
        sales = 0
        purchase = 0
        debt = 0
        for each in sales_data:
            sales += each.grand_total
        for each in purchase_data:
            purchase += each.grand_total
            debt += each.due
        context['sales'] = sales
        context['purchase'] = purchase
        context['debt'] = debt

        # ------------ Top Selling Product
        top_sale = []
        sale_products = ProductLineUp.objects.filter(sale_confirm=True)
        subcategories = SubCategory.objects.all()
        for each in subcategories:
            filterd_products = sale_products.filter(product__subcategory=each)
            if filterd_products:
                product_count = 0
                for each_item in filterd_products:
                    product_count += each_item.quantity
                top_sale.append({
                    f"{each.category}-{each}": product_count
                })
                context['top_sale'] = sorted(top_sale[:5], key=lambda x: list(x.values())[0], reverse=True)[:5]

        # ------------- Stock alert
        for each in products:
            stock_alert_product = products.filter(quantity__lt=each.stock_alert)
        context['stock_alert'] = stock_alert_product

        # ------------- Purchase due
        purchase_due_table = purchases.filter(due__gt=0)
        context['purchase_dues'] = purchase_due_table

        # ------------- Top Selling Brand
        top_brand = []
        brands = Brand.objects.all()
        for each in brands:
            filtered_with_brand = sale_products.filter(product__brand=each)
            if filtered_with_brand:
                product_count = 0
                for each_item in filtered_with_brand:
                    product_count += each_item.quantity
                top_brand.append({
                    f"{each.brand}":product_count
                })
                context['top_brand'] = sorted(top_brand[:5], key=lambda x: list(x.values())[0], reverse=True)[:5]

        
        # ------------ recent sales
        recent_sales = Sales.objects.all()[:15]
        recent_purchase = Purchase.objects.all()[:15]

        context['recent_sales'] = recent_sales
        context['recent_purchase'] = recent_purchase

        return context




# ==========================================SALES SECTION=======================================

# --------------------------------------------------------------- Sales List View
class SalesListView(SuperuserRequiredMixin, ListView):
    model = Sales
    context_object_name = 'Sales'
    template_name = 'inventory/sales/salesList.html'


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
        return context


# --------------------------------------------------------------- New Sale invoice View
class SalesInvoiceListView(SuperuserRequiredMixin, CreateView):
    model = ProductLineUp
    form_class = ProductLineUpForm
    template_name = 'inventory/sales/salesInvoice.html'
    success_url = reverse_lazy('new-sale-invoice')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice_list = self.model.objects.filter(author=self.request.user, sale_confirm=False)
        grand_total = invoice_list.aggregate(grand_total=Sum('subtotal'))['grand_total'] or 0
        context['invoice_list'] = invoice_list
        context['grand_total'] = grand_total
        return context
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        product_code = form.cleaned_data['product_code']
        quantity = form.cleaned_data['quantity']
        product = Product.objects.filter(product_code__icontains=product_code).first()
        obj.author = self.request.user
        obj.product = product
        obj.quantity = quantity
        obj.subtotal = quantity * product.price
        obj.save()
        return super().form_valid(form)
    
#----------------------------------------------------------------- invoice remove item
class InvoiceRemoveItem(SuperuserRequiredMixin, DeleteView):
    model = ProductLineUp
    context_object_name = 'invoiceItem'
    template_name = 'inventory/sales/invoiceRemoveItem.html'
    success_url = reverse_lazy('new-sale-invoice')   



#----------------------------------------------------------------- invoice remove item
class InvoiceUpdateItem(SuperuserRequiredMixin, UpdateView):
    model = ProductLineUp
    form_class = ProductLineUpForm
    context_object_name = 'invoiceItem'
    template_name = 'inventory/sales/invoiceUpdateItem.html'
    success_url = reverse_lazy('new-sale-invoice')

    def get_initial(self):
        initial = super().get_initial()
        obj = self.get_object()
        initial['product_code'] = obj.product.product_code
        return initial
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        product_code = form.cleaned_data['product_code']
        quantity = form.cleaned_data['quantity']
        product = Product.objects.filter(product_code=product_code).first()
        self.object.product = product
        self.object.quantity = quantity
        self.object.subtotal = product.price * quantity
        self.object.save()
        return super().form_valid(form)
    

   
class ConfirmSaleView(SuperuserRequiredMixin, CreateView):
    model = Sales
    form_class = SalesForm
    template_name = 'inventory/sales/salesInvoiceConfirm.html'
    success_url = reverse_lazy('sales-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer_form'] = CustomerForm()
        invoice_list = ProductLineUp.objects.filter(author=self.request.user, sale_confirm=False)
        total_quantity = 0
        for each in invoice_list:
            total_quantity += each.quantity
        grand_total = invoice_list.aggregate(grand_total=Sum('subtotal'))['grand_total'] or 0
        context['grand_total'] = grand_total
        context['total_quantity'] = total_quantity
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.get_form() 
        customer_form = CustomerForm(request.POST)
        invoice_list = ProductLineUp.objects.filter(author=self.request.user, sale_confirm=False)
        grand_total = invoice_list.aggregate(grand_total=Sum('subtotal'))['grand_total'] or 0
        email = customer_form.data.get('email')
        existing_customer = Customer.objects.filter(email=email).first()
        if form.is_valid() and existing_customer:
            sale_instance = form.save(commit=False)
            sale_instance.customer = existing_customer 
            sale_instance.grand_total = grand_total
            sale_instance.save()
            total_quantity = sum(each.quantity for each in invoice_list)
            for each in invoice_list:
                product = Product.objects.filter(product_code=each.product.product_code).first()
                product.quantity -= each.quantity
                product.save()
                each.sale_confirm = True
                each.sale_reference = sale_instance
                each.save()
            sale_instance.total_quantity = total_quantity
            sale_instance.save()
            return HttpResponseRedirect(self.success_url)
        else:
            customer = customer_form.save()
            sale_instance = form.save(commit=False)
            sale_instance.customer = customer
            sale_instance.grand_total = grand_total
            sale_instance.save()
            total_quantity = sum(each.quantity for each in invoice_list)
            for each in invoice_list:
                product = Product.objects.filter(product_code=each.product.product_code).first()
                product.quantity -= each.quantity
                product.save()
                each.sale_confirm = True
                each.sale_reference = sale_instance
                each.save()
            sale_instance.total_quantity = total_quantity
            sale_instance.save()
            return HttpResponseRedirect(self.success_url)
    

def get_filtered_products(request):
    category_id = request.GET.get('category_id')
    brand_id = request.GET.get('brand_id')
    category = Categories.objects.get(id=category_id)
    brand = Brand.objects.get(id=brand_id)
    print(category_id, brand_id)
    products = Product.objects.filter(product__category=category, product__brand=brand).values('id','product__model')
    print(products)
    return JsonResponse({'products': list(products)})




# ==========================================PURCHASE SECTION=======================================
#----------------------------------------------------------------Purchase list view
class PurchaseListView(SuperuserRequiredMixin,ListView):
    model = Purchase
    context_object_name = 'purchases'
    template_name = 'inventory/purchase/purchaseList.html'
    supplier = Supplier.objects.all()
    extra_context = {
        'suppliers': supplier,
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        date = self.request.GET.get('date', None)
        supplier = self.request.GET.get('supplier',None)
        status = self.request.GET.get('status',None)
        payment_status = self.request.GET.get('payment_status',None)

        if date:
            date_object = datetime.strptime(date, "%Y-%m-%d").date()
            queryset = queryset.filter(date_date=date_object)
        if supplier:
            queryset = queryset.filter(supplier=supplier)
        if status:
            queryset = queryset.filter(status=status)
        if payment_status:
            queryset = queryset.filter(payment_status=payment_status)


        if supplier and status and payment_status==None and date==None:
            queryset = queryset.filter(
                Q(supplier=supplier) &
                Q(status=status)
            )
        elif supplier and status==None and payment_status and date==None:
            queryset = queryset.filter(
                Q(supplier=supplier) &
                Q(payment_status=payment_status)
            )
        elif supplier and status==None and payment_status==None and date:
            date_object = datetime.strptime(date, "%Y-%m-%d").date()
            queryset = queryset.filter(
                Q(supplier=supplier) &
                Q(date__date=date_object)
            )
        elif supplier==None and status and payment_status and date==None:
            queryset = queryset.filter(
                Q(status=status) &
                Q(payment_status=payment_status)
            )
        elif supplier==None and status and payment_status==None and date:
            date_object = datetime.strptime(date, "%Y-%m-%d").date()
            queryset = queryset.filter(
                Q(status=status) &
                Q(date__date=date_object)
            )
        elif supplier==None and status==None and payment_status and date:
            date_object = datetime.strptime(date, "%Y-%m-%d").date()
            queryset = queryset.filter(
                Q(payment_status=payment_status) &
                Q(date__date=date_object)
            )
        elif supplier and status and payment_status and date==None:
            queryset = queryset.filter(
                Q(supplier=supplier) &
                Q(status=status) &
                Q(payment_status=payment_status)
            )
        elif supplier and status and payment_status==None and date:
            date_object = datetime.strptime(date, "%Y-%m-%d").date()
            queryset = queryset.filter(
                Q(supplier=supplier) &
                Q(status=status) &
                Q(date__date=date_object)
            )
        elif supplier and status==None and payment_status and date:
            date_object = datetime.strptime(date, "%Y-%m-%d").date()
            queryset = queryset.filter(
                Q(supplier=supplier) &
                Q(status=status) &
                Q(date__date=date_object)
            )
        elif supplier==None and status and payment_status and date:
            date_object = datetime.strptime(date, "%Y-%m-%d").date()
            queryset = queryset.filter(
                Q(status=status) &
                Q(payment_status=payment_status) &
                Q(date__date=date_object)
            )
        elif supplier and status and payment_status and date:
            date_object = datetime.strptime(date, "%Y-%m-%d").date()
            queryset = queryset.filter(
                Q(supplier=supplier) &
                Q(status=status) &
                Q(payment_status=payment_status) &
                Q(date__date=date_object)
            )
        return queryset


# --------------------------------------------------------------- new Purchase view
class PurchaseLinpUpView(SuperuserRequiredMixin,CreateView):
    model = PurchaseLineUp
    form_class = PurchaseLinuUpForm
    template_name = 'inventory/purchase/purchaseInvoice.html'
    success_url = reverse_lazy('new-purchase-invoice')

    def get(self, request, *args, **kwargs):
        form = PurchaseLinuUpForm()
        form2 = PurchaseLineUpform2()
        invoice_list = PurchaseLineUp.objects.filter(author=self.request.user, purchase_confirm=False)
        grand_total = invoice_list.aggregate(total_subtotal=Sum('subtotal'))['total_subtotal'] or 0
        return render(request, self.template_name, {'form': form, 'form2': form2, 'invoice_list': invoice_list, 'grand_total': grand_total})
    
    def post(self, request, *args, **kwargs):
        form = PurchaseLinuUpForm(request.POST)
        form2 = PurchaseLineUpform2(request.POST)
        
        if form.is_valid() and form.cleaned_data.get('product_name'):
            form.instance.author = self.request.user
            form.save()
            return redirect(self.success_url)
        
        if form2.is_valid() and form2.cleaned_data.get('product_code'):
            form2.instance.author = self.request.user
            form2.save()
            return redirect(self.success_url)
        
        return render(request, self.template_name, {'form': form, 'form2': form2})



def get_filtered_subcategory(request):
    category_id = request.GET.get('category_id')
    category = Categories.objects.get(id=category_id)
    subcategory = SubCategory.objects.filter(category=category).values('id','name')
    return JsonResponse({'subcategory': list(subcategory)})


# --------------------------------------------------------------- new Purchase view
class PurchaseInvoiceEditView(SuperuserRequiredMixin,UpdateView):
    model = PurchaseLineUp
    form_class = PurchaseLinuUpForm
    template_name = 'inventory/purchase/purchaseInvEdit.html'
    success_url = reverse_lazy('new-purchase-invoice')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super().form_valid(form)


# --------------------------------------------------------------- new Purchase view
class PurchaseInvoiceDeleteView(SuperuserRequiredMixin,DeleteView):
    model = PurchaseLineUp
    context_object_name = 'item'
    template_name = 'inventory/purchase/purchaseInvRemove.html'
    success_url = reverse_lazy('new-purchase-invoice')


# --------------------------------------------------------------- Purchase confirm view
class PurchaseConfirmView(SuperuserRequiredMixin, CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'inventory/purchase/purchaseConfirm.html'
    success_url = reverse_lazy('purchase-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['supplier_form'] = SupplierForm()
        invoice_list = PurchaseLineUp.objects.filter(author=self.request.user, purchase_confirm=False)
        total_quantity = 0
        for each in invoice_list:
            total_quantity += each.quantity
        grand_total = invoice_list.aggregate(grand_total=Sum('subtotal'))['grand_total'] or 0
        context['grand_total'] = grand_total
        context['total_quantity'] = total_quantity
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()  # Retrieve the PurchaseForm
        supplier_form = SupplierForm(request.POST)
        invoice_list = PurchaseLineUp.objects.filter(author=self.request.user, purchase_confirm=False)
        grand_total = invoice_list.aggregate(grand_total=Sum('subtotal'))['grand_total'] or 0
        email = supplier_form.data.get('email')
        existing_supplier = Supplier.objects.filter(email=email).first()
        if form.is_valid() and existing_supplier:
            supplier_instance = existing_supplier
            purchase_instance = form.save(commit=False)
            purchase_instance.supplier = supplier_instance 
            purchase_instance.grand_total = grand_total
            purchase_instance.save()
            for each in invoice_list:
                if not each.product:
                    new_product = Product.objects.create(
                        category = each.category,
                        subcategory = each.subcategory,
                        brand = each.brand,
                        product_name = each.product_name,
                        cost = each.unit_price,
                        quantity=each.quantity
                    )
                    new_product.save()
                else:
                    each.product.quantity += each.quantity
                    each.product.save()
                each.purchase_confirm = True
                each.purchase_reference = purchase_instance
                each.save()
            return HttpResponseRedirect(self.success_url)
        else:
            supplier_instance = supplier_form.save()
            purchase_instance = form.save(commit=False)
            purchase_instance.supplier = supplier_instance 
            purchase_instance.grand_total = grand_total
            purchase_instance.save()
            for each in invoice_list:
                if not each.product:
                    new_product = Product.objects.create(
                        category = each.category,
                        subcategory = each.subcategory,
                        brand = each.brand,
                        product_name = each.product_name,
                        cost = each.unit_price,
                        quantity=each.quantity
                    )
                    new_product.save()
                else:
                    each.product.quantity += each.quantity
                each.purchase_confirm = True
                each.purchase_reference = purchase_instance
                each.save()
            return HttpResponseRedirect(self.success_url)



# --------------------------------------------------------------- Purchase details view
class PurchaseDetailsView(SuperuserRequiredMixin,DetailView):
    model = Purchase
    context_object_name = 'purchase'
    template_name = 'inventory/purchase/purchaseDetails.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchase = self.get_object()
        invoice_list = PurchaseLineUp.objects.filter(purchase_reference = purchase, purchase_confirm=True)
        grand_total = invoice_list.aggregate(grand_total=Sum('subtotal'))['grand_total'] or 0
        context['invoice_list'] = invoice_list
        context['grand_total'] = grand_total
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

    def post(self, request, *args,**kwargs):
        purchase = self.get_object()
        invoice = PurchaseLineUp.objects.filter(purchase_reference=purchase)
        invoice.delete()
        return super().post(request, *args, **kwargs)
    
    

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
        category = self.request.GET.get('category', None)
        subcategory = self.request.GET.get('subcategory',None)
        brand = self.request.GET.get('brand',None)
        status = self.request.GET.get('status',None)
        max_price = self.request.GET.get('max_price',None)
        min_price = self.request.GET.get('min_price',None)

        if search_query:
            queryset = queryset.filter(
                Q(product_name__icontains=search_query) |
                Q(product_code=search_query)
            )
        if category:
            queryset = queryset.filter(category__id=category)
            if subcategory and subcategory != "0":
                queryset = queryset.filter(subcategory__id=subcategory)
        if brand:
            queryset = queryset.filter(brand__id=brand)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
           
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_id = self.kwargs.get('pk',None)
        product = Product.objects.filter(id=object_id).first()
        product_image = Product_Image.objects.filter(product=product)
        context['Images'] = product_image
        context['form'] = ProductImageForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            product = self.get_object()
            product_image = form.save(commit=False)
            product_image.product = product
            product_image.save()
            return redirect('product-details', pk=product.pk)  # Redirect to product details page after successful upload
        else:
            context = self.get_context_data(form=form)
            return render(request, self.template_name, context)

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_id = self.kwargs.get('pk',None)
        product = Product.objects.filter(id=object_id).first()
        print("product",product)
        product_image = Product_Image.objects.filter(product=product).first()
        print("image:",product_image)
        context['product_image'] = product_image
        return context



# ==========================================CATEGORY SECTION=======================================
# ---------------------------------------------------------------Category Create view and list view
class CategoryView(SuperuserRequiredMixin,CreateView):
    model = Categories
    form_class = CategoryForm
    template_name = 'inventory/category/category.html'
    success_url = reverse_lazy('category-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = self.model.objects.all()
        search_query = self.request.GET.get('q', None)
        if search_query:
            categories = categories.filter(category__icontains=search_query)
        categories = categories.annotate(subcategory_count=Count('subcategory'))
        context['categories'] = categories
        return context


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


# --------------------------------------------------------------- sub category create and list view
class SubcategoryView(SuperuserRequiredMixin,CreateView):
    model = SubCategory
    form_class = SubCategoryForm
    context_object_name = 'subcategories'
    template_name = 'inventory/category/subcategory.html'

    def get_success_url(self, **kwargs) -> str:
        category = self.kwargs.get('pk',None)
        return reverse('sub-categories', kwargs={'pk': category})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        category = self.kwargs.get('pk',None)
        Category = Categories.objects.filter(category=category).first()
        self.object.category = Category
        self.object.save()
        return super().form_valid(form)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs.get('pk',None)
        category_instance = Categories.objects.filter(category=category).first()
        subcategories = self.model.objects.filter(category = category_instance)
        search_query = self.request.GET.get('q', None)
        if search_query:
            subcategories = subcategories.filter(name__icontains=search_query)
        subcategories = subcategories.annotate(product_count=Count('product'))
        context['category'] = category
        context['subcategories'] = subcategories
        return context
    

# ==========================================BRAND SECTION=======================================
# ---------------------------------------------------------------Brand list view
class BrandListView(SuperuserRequiredMixin,CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'inventory/brand/brandList.html'
    success_url = reverse_lazy('brand-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand = self.model.objects.all()
        search_query = self.request.GET.get('q', None)
        if search_query:
            brand = brand.filter(brand__icontains=search_query)
        context['brands'] = brand
        return context


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
    template_name = 'inventory/reports/report.html'



# ==========================================SUPPLIERS SECTION=======================================
# ---------------------------------------------------------------Supplier List view
class SuppliersListView(SuperuserRequiredMixin,ListView):
    model = Supplier
    context_object_name = 'suppliers'
    template_name = 'inventory/suppliers/supplierList.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', None)
        if search_query:
            queryset = queryset.filter(
                Q(company_name__icontains = search_query) | 
                Q(contact_person__icontains = search_query) |
                Q(email__icontains = search_query) |
                Q(phone_number__icontains = search_query) 
            )
        return queryset

# ---------------------------------------------------------------Supplier create view
class SupplierCreateView(SuperuserRequiredMixin,CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'inventory/suppliers/supplierCreate.html'
    success_url = reverse_lazy('supplier-list')

# ---------------------------------------------------------------Supplier update view
class SupplierUpdateView(SuperuserRequiredMixin,UpdateView):
    model = Supplier
    form_class = SupplierForm
    context_object_name = 'supplier'
    template_name = 'inventory/suppliers/supplierUpdate.html'
    success_url = reverse_lazy('supplier-list')

# ---------------------------------------------------------------Supplier delete view
class SupplierDeleteView(SuperuserRequiredMixin,DeleteView):
    model = Supplier
    form_class = SupplierForm
    context_object_name = 'supplier'
    template_name = 'inventory/suppliers/supplierDelete.html'
    success_url = reverse_lazy('supplier-list')



# ==========================================ORDER SECTION=======================================
class OrderView(SuperuserRequiredMixin,TemplateView):
    template_name = 'inventory/orders/order.html'


# ==========================================MANAGE STORE SECTION=======================================
class StoreManageView(SuperuserRequiredMixin,TemplateView):
    template_name = 'manage/index.html'