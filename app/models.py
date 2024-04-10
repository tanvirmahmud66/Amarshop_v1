from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
import os

# Create your models here.
#============================================================================= Custom user Model
class UserManager(BaseUserManager):
    def create_user(self, email,password=None, **extra_fields):
        if not email:
            raise ValueError("user must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None,**extra_fields):
        if not email:
            raise ValueError("user must have an email address")
        email = self.normalize_email(email)
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


def profile_image_path(instance, filename):
    return os.path.join('Admin_profile_images', f'{instance.email}', filename)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to=profile_image_path, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
    
    


# =========================================================================== Device Categories Model
class Categories(models.Model):
    category = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.category
    


#============================================================================ Brand Model 
class Brand(models.Model):
    brand = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['-id']
    
    def __str__(self):
        return self.brand




#============================================================================ Devices Model
def product_image_path(instance, filename):
    return os.path.join('Product_Image', f'{instance.model}', filename)


class Product(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.CharField(max_length=255)
    cost = models.PositiveIntegerField(null=True,blank=True)
    price = models.PositiveIntegerField(null=True,blank=True)
    description = models.TextField(null=True, blank=True)
    productImg = models.ImageField(upload_to=product_image_path, null=True, blank=True,)
    released_year = models.DateField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.model
    
    

#=============================================================================== supplier model
class Supplier(models.Model):
    company_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.company_name


#=================================================================================== Inventory Model
class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, unique=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField(null=True,blank=True)
    unit_cost = models.PositiveIntegerField()
    total_cost = models.PositiveBigIntegerField(null=True, blank=True)
    valuation = models.PositiveBigIntegerField(null=True, blank=True)
    profit = models.PositiveBigIntegerField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_cost = self.quantity * self.unit_cost
        if self.unit_price:
            product = Product.objects.get(id=self.product.id)
            if product:
                product.price = self.unit_price
            self.valuation = self.quantity * self.unit_price
            self.profit = self.valuation - self.total_cost
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.product.model


#============================================================================ Purchase Model
class Purchase(models.Model):
    PAYMENT_METHOD = [
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
    ]

    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit_cost = models.PositiveIntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    transaction_type = models.CharField(max_length=10,null=True,blank=True,default='OUT')
    payment_method = models.CharField(max_length=50,choices=PAYMENT_METHOD)
    paid_ammount = models.PositiveBigIntegerField()
    reference = models.CharField(max_length=100,null=True,blank=True) 
    due_amount = models.PositiveBigIntegerField(default=0)
    purchase_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-purchase_date']

    def save(self, *args, **kwargs):
        self.due_amount = (self.quantity*self.unit_cost) - self.paid_ammount
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.model


# =========================================================== Generel User
class GeneralUser(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True,null=True, blank=True)
    phone = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ['-id']
    
    def __str__(self):
        return f"{self.id}"



# ============================================================ Sales Model
class Sales(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)
    general_user = models.ForeignKey(GeneralUser, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.IntegerField(null=True,blank=True)
    product_quantity = models.BigIntegerField(null=True,blank=True)
    sales_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sales_date']

    def __str__(self):
        return f"{self.id}"



# ============================================================ Product Line up Model
class ProductLineUp(models.Model):
    token = models.CharField(max_length=100, blank=True)
    product = models.ForeignKey(Inventory, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveBigIntegerField(null=True,blank=True)
    sale_confirm = models.BooleanField(default=False)
    sale_reference = models.ForeignKey(Sales, on_delete=models.CASCADE, null=True,blank=True)
    

    def __str__(self):
        return self.product.product.model




#============================================================================== Transaction Model
class Transaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
    sale = models.ForeignKey(Sales, on_delete=models.CASCADE,null=True,blank=True)
    transaction_type = models.CharField(max_length=5)
    payment_method = models.CharField(max_length=50,)
    amount = models.PositiveBigIntegerField()
    reference = models.CharField(max_length=100,null=True,blank=True)
    transaction_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.id}"