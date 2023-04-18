from django.db import models
import random
# from django.utils import timezone #after opting 2 in published for default for existing ones
from django.utils.text import slugify
from django.db.models.signals import pre_save,post_save
from django.urls import reverse
from django.db.models import Q
from django.conf import settings


# Create your models here.

User = settings.AUTH_USER_MODEL

class ArticleQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.none()
        lookups = Q(title__icontains=query) | Q(content__icontains=query)
        return self.filter(lookups) 

class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class Article(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=120)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)  # to add the timestamp
    # to add the updated timestamp
    updated = models.DateTimeField(auto_now=True)
    # publish=models.DateField(auto_now_add=False,auto_now=False,default=timezone.now)#to add the published timestamp,can be True can qutomatically assigned

    # #if we want to keep the published field blank
    publish = models.DateField(
        null=True, blank=True
    )  # (null for databadse and blank for Django) & it does not affects the publishing field in existing models.

    # (null for databadse and blank for Django)
    slug = models.SlugField(unique=True,blank=True, null=True)



    #Added for home_view (and detail.html)
    def get_absolute_url(self):
        return f'/articles/{self.slug}/'
    
    def reverse_url(self):
         return reverse("article-detail", kwargs={"slug": self.slug})

    objects=ArticleManager() #for more complex search to make things more ROBUST (qs = Article.objects.search(query=query))
    

# save krne ke sath hi slug bhi set ho jayega
    def save(self, *args, **kwargs):
        #pre_save and post_save me use krne ke liye comment kr diye h
        # if self.slug is None:
        #   self.slug = slugify(self.title)
        super().save(*args, **kwargs)


#post_save and pre_save signals save ke saath hi kaam karega
#pre_save save ke pehle and post_save signal save ke baad

#ek baar check krne  ke liye saare slugs None kr dena
# python manage.py shell
# from articles.models import Article
# for obj in Article.objects.all(): 
#          obj.slug=None
#          obj.save()


def slugify_instance_title(instance,save=False,new_slug=None):

    if new_slug is not None:
        slug = new_slug

    else:
       slug = slugify(instance.title)
    
    qs = Article.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        rand_int = random.randint(300_000, 500_000)
        slug = f"{slug}-{rand_int}"
        return slugify_instance_title(instance, save=save,new_slug=slug)
    instance.slug = slug

    if save:
        instance.save()
    
    return instance
    

def article_pre_save(sender,instance,*args,**kwargs):
    print("pre_save")
    if instance.slug is None:
        # instance.slug = slugify(instance.title)
        slugify_instance_title(instance,save=False)

pre_save.connect(article_pre_save,sender = Article)

def article_post_save(sender,instance,created,*args,**kwargs):
    print("post_save")
    if created: #created == true , kewal ek baar new article bnate samay hi true hoga bs,phir baar-2 nhi ,jisse repetitions ruk jaega
        # instance.slug = "this is the new slug for newly created article."

        # instance.slug = slugify(instance.title)
        # instance.save()

        slugify_instance_title(instance,save=True)

post_save.connect(article_post_save,sender=Article)







# yha par kuch bhi change kene par
# python manage.py makemigrations
# python manage.py migrate
# command run kr dena

# isko use krne ke liye
# pip install dataclasses,may be

