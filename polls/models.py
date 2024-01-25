from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=11)
    description = models.TextField()
    
    def __str__(self):
        return f' Message from {self.name}'
    


class Blogs(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    authname = models.CharField(max_length=50)
    img = models.ImageField(upload_to = 'pics', blank = True, null = True)
    timeStamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f' uploaded by {self.authname}'