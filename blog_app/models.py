from django.db import models
from account.models import User

class Blog(models.Model):
    title= models.CharField(max_length=100, blank= False, null=False)
    author= models.ForeignKey(User, on_delete= models.CASCADE)
    description= models.TextField(blank=False,null= False)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    image= models.ImageField(upload_to = "images/", blank=True, null = True)
    
    def __str__(self):
        return self.title

