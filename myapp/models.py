from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=60)
    email=models.EmailField(unique=True)
    mobile=models.BigIntegerField(unique=True)
    password=models.CharField(max_length=10)
    profile=models.ImageField(default="",upload_to="profile/")
    usertype=models.CharField(max_length=20,default="buyer")
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}" 
    

class Product(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    category=(
        ("cloth","cloth"),
        ("googles","googles"),
        ("watch","watch"),

    )
    company=(
        ("nike","nike"),
        ("puma","puma"),
        ("rolex","rolex"),

    )
    pcategory=models.CharField(max_length=20,choices=category)
    pcompany=models.CharField(max_length=30,choices=company)

    pname=models.CharField(max_length=30)
    pprice=models.IntegerField()
    pdesc=models.TextField()
    pimage=models.ImageField(default="",upload_to="product/")

    def __str__(self):
        return f"{self.pname}"
    

class Whishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    ttime=models.DateTimeField(default=timezone.now())


    def __str__(self):
        return f"{self.user}"

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    ttime=models.DateTimeField(default=timezone.now())
    total=models.PositiveIntegerField()
    qty=models.PositiveIntegerField(default=1)
    payment=models.BooleanField(default=False)


    def __str__(self):
        return f"{self.product}"
