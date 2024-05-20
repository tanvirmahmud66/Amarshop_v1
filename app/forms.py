from django import forms
from django.contrib.auth.forms import UserCreationForm
from multiupload.fields import MultiFileField
from .models import (
    User,
    AdminProfile,
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
            admin_profile = AdminProfile.objects.create(user=user)
            admin_profile.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = User.objects.create_user(email, password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)  # Ensure the proper database is used
        return user


# -------------------------------------- Profile Picture Form
class AdminProfilePictureForm(forms.ModelForm):
    class Meta:
        model = AdminProfile
        fields = ['profile_pic']


# -------------------------------------- Profile Picture Form
class AdminUpdateForm(forms.ModelForm):
    class Meta:
        model = AdminProfile
        fields = ['phone','nid','address1','address2']



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



