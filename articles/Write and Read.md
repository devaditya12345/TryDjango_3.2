(try-django) PS C:\Users\Aditya\Desktop\WEBD\Django\try-django> python manage.py shell
Python 3.6.8 (tags/v3.6.8:3c6b436a57, Dec 24 2018, 00:16:47) [MSC v.1916 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)


>>> from articles.models import Article

# write
>>> obj=Article()
>>> obj.title
''
>>> obj.content
''


>>> obj=Article(title='This is the first title',content='This is the first content')
>>> obj.save()
>>> obj.title
'This is the first title'
>>> obj.content
'This is the first content'
>>> obj.id
1
>>> obj
<Article: Article object (1)>

# Another way of write and save instantly
>>> obj1=Article.objects.create(title='This is the second title',content='This is the second content')
>>> obj1.title
'This is the second title'
>>> obj1.content
'This is the second content'
>>> obj1
<Article: Article object (2)>
>>> obj1.id
2

# Read and write 
>>> obj3=Article.objects.get(id=1)
>>> obj3.title
'This is the first title'
>>> obj3.content
'This is the first content'
>>> obj3.save()  //Bina save kiye bhi store ho jayega ye
>>> obj3
<Article: Article object (1)>
>>> obj3.id
1
>>> obj.id
1
>>> obj1.id
2