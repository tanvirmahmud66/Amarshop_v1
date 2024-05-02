import uuid
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
from django.urls import reverse
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
    

# =========================================================== Customer
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=255, null=True,blank=True)
    email = models.EmailField(max_length=255, unique=True,null=True, blank=True)
    phone = models.CharField(max_length=20)
    address = models.TextField(max_length=100,null=True, blank=True)
    
    class Meta:
        ordering = ['-id']
    
    def __str__(self):
        return f"{self.id}"

# =========================================================================== admin panel Profile
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    about = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.user


# =========================================================================== Device Categories Model
class Categories(models.Model):
    category = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.category
    


# ========================================================================== Sub Category model
class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']
    
    def __str__(self):
        return self.name


#============================================================================ Brand Model 
class Brand(models.Model):
    brand = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['-id']
    
    def __str__(self):
        return self.brand




#============================================================================ Product Model
def qr__image_path(instance, filename):
    return os.path.join('Product_barcode', f'{instance.id}_{instance.product_name}', filename)


class Product(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE,null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_code = models.CharField(max_length=20,null=True,blank=True)
    quantity = models.PositiveIntegerField(null=True,blank=True)
    stock_alert = models.PositiveIntegerField(default=5)
    cost = models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    price = models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    description = models.TextField(null=True, blank=True)
    barcode = models.ImageField(upload_to=qr__image_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.product_code:
            product_uuid = uuid.uuid4()
            product_number = int(product_uuid.int)
            product_code = str(product_number)[:7]
            self.product_code = product_code

        # Generate barcode
        barcode_value = self.product_code  # Use product code as barcode value
        code128 = barcode.get_barcode_class('code128')
        barcode_instance = code128(barcode_value, writer=ImageWriter())
        
        # Save barcode image to BytesIO buffer
        buffer = BytesIO()
        barcode_instance.write(buffer)
        filename = f'barcode-{self.id}.png'
        self.barcode.save(filename, File(buffer), save=False)

        super().save(*args, **kwargs)
    
    def __str__(self):
        return str(self.id)
    

# ============================================================================== Product Img Model
def Image_path(instance, filename):
    return os.path.join('Product_Image', f'{instance.product.id}_{instance.product.product_name}', filename)

class Product_Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=Image_path,null=True, blank=True)

    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return str(self.id)


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
    STATUS = [
        ('Received','Received'),
        ('Ordered','Ordered'),
        ('Pending','Pending'),
    ]
    PAYMENT_STATUS = [
        ('Paid','Paid'),
        ('Due','Due'),
        ('Partial','Partial')
    ]

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=50,choices=STATUS)
    payment_status = models.CharField(max_length=50,choices=PAYMENT_STATUS)
    payment_method = models.CharField(max_length=50,choices=PAYMENT_METHOD)
    grand_total = models.DecimalField(max_digits=12,decimal_places=2)
    paid = models.DecimalField(max_digits=12,decimal_places=2)
    due = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    date = models.DateField(auto_now_add=True)
    total_discount = models.DecimalField(max_digits=12,decimal_places=2,default=0,null=True,blank=True)
    total_tax = models.DecimalField(max_digits=12,decimal_places=2,default=0,null=True,blank=True)
    shipping = models.DecimalField(max_digits=12,decimal_places=2,default=0,null=True,blank=True)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        self.due = self.grand_total - self.paid 
        super().save(*args, **kwargs)
    
    def __str__(self):
        return str(self.id)



# ============================================================ Purchase Line up
class PurchaseLineUp(models.Model):
    author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=255,null=True,blank=True)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL,null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory,on_delete=models.SET_NULL,null=True,blank=True)
    brand = models.ForeignKey(Brand,on_delete=models.SET_NULL,null=True,blank=True)
    unit_price = models.DecimalField(max_digits=12,decimal_places=2)
    quantity = models.IntegerField()
    subtotal = models.DecimalField(max_digits=12,decimal_places=2)
    discount = models.DecimalField(max_digits=12,default=0, decimal_places=2,null=True,blank=True)
    tax = models.DecimalField(max_digits=12, default=0,null=True,blank=True,decimal_places=2)
    purchase_confirm = models.BooleanField(default=False)
    purchase_reference = models.ForeignKey(Purchase,on_delete=models.CASCADE,null=True,blank=True)

    def save(self,*args, **kwargs):
        subtotal = (self.unit_price * self.quantity)
        discount_amount = subtotal * (self.discount/100)
        discount_subtotal = subtotal - discount_amount
        tax_amount = discount_subtotal * (self.tax/100)
        self.subtotal = discount_subtotal + tax_amount
        super().save(*args,**kwargs)

    def __str__(self):
        return str(self.id)





# ============================================================ Sales Model
class Sales(models.Model):
    STATUS = [
        ('Delivered','Delivered'),
        ('Ordered','Ordered'),
        ('Pending','Pending'),
    ]
    PAYMENT_STATUS = [
        ('Paid','Paid'),
        ('Due','Due'),
        ('Partial','Partial')
    ]
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,null=True, blank=True)
    total_quantity = models.BigIntegerField(null=True,blank=True)
    grand_total = models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    paid = models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    due = models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    status = models.CharField(max_length=50,choices=STATUS,null=True,blank=True)
    payment_status = models.CharField(max_length=50,choices=PAYMENT_STATUS,null=True,blank=True)
    sales_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sales_date']

    def save(self, *args, **kwargs):
        self.due = self.grand_total - self.paid 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}"



# ============================================================ Product Line up Model
class ProductLineUp(models.Model):
    author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    sale_confirm = models.BooleanField(default=False)
    sale_reference = models.ForeignKey(Sales, on_delete=models.CASCADE, null=True,blank=True)
    

    def __str__(self):
        return str(self.id)


