from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    phone = models.IntegerField(blank=True,null=True)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to='shop/images', default="")

    def __str__(self):
        return self.product_name


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")


    def __str__(self):
        return self.name

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    amount = models.IntegerField( default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=111)
    address = models.CharField(max_length=111)
    city = models.CharField(max_length=111)
    state = models.CharField(max_length=111)
    zip_code = models.CharField(max_length=111)
    phone = models.CharField(max_length=111, default="")

class OrderUpdate(models.Model):
    update_id  = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."


class BookMechanic(models.Model):
    # Create a booked field in BookMechanic
    mec_img = models.ImageField(upload_to='shop/mechanic')
    name = models.CharField(max_length=400)
    email = models.EmailField(blank=True,null=True)
    age = models.IntegerField()
    experience = models.TextField()
    phone = models.IntegerField()
    address = models.TextField()

class User_Signup(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='user_content')
    booked_mechanic = models.ForeignKey(BookMechanic,on_delete=models.CASCADE,null=True)
    image = models.ImageField(upload_to='profile_photo/',null=True)
    phone = models.IntegerField()
    mobile = models.IntegerField()
    age = models.PositiveIntegerField()
    address = models.TextField()




