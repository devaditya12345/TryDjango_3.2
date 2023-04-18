from django.contrib import admin

# Register your models here.

from .models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id','title','timestamp','updated','slug']
    search_fields = ['title','content','id']
admin.site.register(Article,ArticleAdmin)
