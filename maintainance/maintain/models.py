from django.db import models

# Create your models here.
class Catagory(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Speciality(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Asset(models.Model):
    name = models.CharField(max_length=100,default='unnamed asset')
    owner_name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    catagory = models.ForeignKey(Catagory,on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return self.name

class Technician(models.Model):
    name = models.CharField(max_length=100)
    Speciality = models.ForeignKey(Speciality,on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return self.name

class Order(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/')
    asset = models.ForeignKey(Asset,on_delete=models.CASCADE)
    technician = models.ForeignKey(Technician,on_delete=models.SET_NULL,null=True)
    visibility = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
class Comment(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    email = models.EmailField(('user email'),max_length=300)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

class client(models.Model):
    name = models.CharField(max_length=50)
    fname = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    