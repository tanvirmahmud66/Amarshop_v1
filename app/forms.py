from django import forms
from django.contrib.auth.forms import UserCreationForm
from multiupload.fields import MultiFileField
from .models import (
    User,
    Customer,
    Profile,
    Categories,
    SubCategory,
    Brand, 
    Transaction,
    Product, 
    Product_Image,
    Supplier,
    Purchase,
    PurchaseLineUp,
    ProductLineUp,
    Sales
)

# ---------------------------------------Admin create Form
class AdminCreateForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=(('staff', 'Staff'), ('superuser', 'Admin')), initial='', widget=forms.Select())
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('user_type'):
            user_type = self.cleaned_data.get('user_type')
            if user_type == 'staff':
                user.is_staff = True
            elif user_type == 'superuser':
                user.is_staff=True
                user.is_superuser = True
        
        if commit:
            user.save()
            profile = Profile.objects.create(user=user)
            profile.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = User.objects.create_user(email, password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)  # Ensure the proper database is used
        return user

# # ------------------------------------------------- customer create form
# class CustomerCreateForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('name', 'email', 'phone','address')

#     def save(self, commit=True):
#         user = super().save()
#         if commit:
#             user.save()
#         return user

# -------------------------------------- Profile Picture Form
class UserProfilePictureForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_pic']


# -------------------------------------- Profile Picture Form
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['about','phone','address']


# -------------------------------------- Category Form
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = '__all__'


# -------------------------------------- Sub category Form
class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['name']

# --------------------------------------- Brand Form
class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'


# --------------------------------------- Product Form
class Productform(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name','category','subcategory','brand','quantity','stock_alert','cost','price','description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}), 
        }

# ---------------------------------------- Product image form
class ProductImageForm(forms.ModelForm):
    class Meta:
        model = Product_Image
        fields= ['image']

# ---------------------------------------- Supplier Form
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'
        widgets = {
            'address': forms.Textarea(attrs={'rows': 5}),
        }


# ---------------------------------------- Purchase Form
class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['status','payment_method','paid', 'payment_status','shipping']
        

#  --------------------------------------- Purchase Lineup Form
class PurchaseLinuUpForm(forms.ModelForm):
    class Meta:
        model = PurchaseLineUp
        fields = ['product_name','category','subcategory','brand','unit_price','quantity', 'discount','tax']


# ---------------------------------------- Purchase Lineup form 2
class PurchaseLineUpform2(forms.ModelForm):
    product_code = forms.CharField(max_length=100)

    class Meta:
        model = PurchaseLineUp
        fields = ['product_code','unit_price','quantity','discount','tax']
    
    def save(self, commit=True):
        instance = super(PurchaseLineUpform2, self).save(commit=False)
        product_code = self.cleaned_data['product_code']
        product = Product.objects.filter(product_code=product_code).first()
        instance.product = product
        if commit:
            instance.save()
        return instance

# ------------------------------------------ General Form
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','email','phone']


# ------------------------------------------ Product Line up form
class ProductLineUpForm(forms.ModelForm):
    product_code = forms.CharField(max_length=100)

    class Meta:
        model = ProductLineUp
        fields = ['product_code','quantity']

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_code'].queryset = Product.objects.all()


# --------------------------------------------- Sales Form
class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = ['paid','payment_status']


# ---------------------------------------------- Transaction Form
class TransactionForm(forms.ModelForm):

    PAYMENT_METHOD = (
        ('Cash', 'Cash'),
        ('Credit Card', 'Credit card'),
        ('Master Card', 'Master Card'),
        ('Bank Cheque','Bank cheque'),
        ('Bkash','Bkash'),
        ('Sure Cash','Sure Cash'),
        ('DBBL Mobile','DBBL Mobile'),
        ('DBBL Card','DBBL Card'),
        ('Nagad','Nagad'),
        ('UCash', 'UCash'),
        ('Payoneer','Payoneer'),
    )

    payment_method = forms.ChoiceField(choices=PAYMENT_METHOD)

    class Meta:
        model = Transaction
        fields = ['payment_method','amount']
