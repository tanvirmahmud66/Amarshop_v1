from django import forms
from django.contrib.auth.forms import UserCreationForm
from multiupload.fields import MultiFileField
from .models import (
    User,
    Categories,
    Brand, 
    Inventory, 
    Transaction,
    Product, 
    Supplier,
    Purchase,
    GeneralUser,
    ProductLineUp,
    Sales
)

# ---------------------------------------Admin create Form
class AdminCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        user.is_superuser = True
        if commit:
            user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = User.objects.create_user(email, password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)  # Ensure the proper database is used
        return user

# -------------------------------------- Profile Picture Form
class UserProfilePictureForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_pic']


# -------------------------------------- Profile Picture Form
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']


# -------------------------------------- Category Form
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = '__all__'


# --------------------------------------- Brand Form
class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'


# --------------------------------------- Inventory Form
class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'

class InventoryPriceSetForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['unit_price']


# --------------------------------------- Product Form
class Productform(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}), 
            'released_year': forms.SelectDateWidget(years=range(2018, 2030))
        }


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
        fields = ['category','brand','model','quantity','unit_cost','supplier','payment_method','paid_ammount','reference']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 1})
        }
    

# ------------------------------------------ General Form
class GeneralUserForm(forms.ModelForm):
    class Meta:
        model = GeneralUser
        fields = '__all__'


# ------------------------------------------ Product Line up form
class ProductLineUpForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Categories.objects.all(), required=False)
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), required=False)

    class Meta:
        model = ProductLineUp
        fields = ['product','quantity']

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Inventory.objects.all()


# --------------------------------------------- Sales Form
class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = '__all__'


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
