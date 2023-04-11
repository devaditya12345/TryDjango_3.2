from django.db import models
# from django.utils import timezone #after opting 2 in published for default for existing ones

# Create your models here.

class Article(models.Model):
    title=models.CharField(max_length=120)
    content=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)#to add the timestamp
    updated=models.DateTimeField(auto_now=True)#to add the updated timestamp
    # publish=models.DateField(auto_now_add=False,auto_now=False,default=timezone.now)#to add the published timestamp,can be True can qutomatically assigned

    #if we want to keep the published field blank 
    publish=models.DateField(auto_now_add=False,auto_now=False,null=True,blank=True) #(null for databadse and blank for Django) & it doesnot affects the publishing field in existing models.


# yha par kuch bhi change kene par 
# python manage.py makemigrations
# python manage.py migrate
# command run kr dena

# isko use krne ke liye
# pip install dataclasses