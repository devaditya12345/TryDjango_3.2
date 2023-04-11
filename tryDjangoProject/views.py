'''
To render HTML Webpages
'''

from django.http import HttpResponse
import random
from articles.models import Article 
from django.template.loader import render_to_string

# HTML_STRING="""
# <h1>Hello World!</h1>
# <h1>This is a View Page(helps to render HTML on the Django's Requests)
# """

name="Aditya"
rand_id=random.randint(1,4)

def home_view(request):
    """
    Take Django requests
    and Return Rendered HTML as response.
    """

    # H1=f"""
    # <h1>Hello {name}!</h1>
    # """

    # P1 = f"""
    # <p1>This is a number {number}</p1>
    # """
    # HTML_STRING=H1+P1

    #from the database

    # article_obj=Article.objects.get(id=2)
    # article_obj=Article.objects.get(id=rand_id)

    # H1=f"""
    # <h1>Hello {article_obj.title}!.</h1>
    # """

    # P1 = f"""
    # <p1>{article_obj.content} having id {article_obj.id}.</p1>
    # """
    # HTML_STRING=H1+P1

    # article_obj=Article.objects.get(id=rand_id)

    # HTML_STRING=f"""
    # <h1>Hello {article_obj.title}!.</h1>
    # <p1>{article_obj.content} having id {article_obj.id}.</p1>
    # """

    # print(rand_id)
    article_obj=Article.objects.get(id=rand_id)
    # article_obj=Article.objects.get(int(float('5.000')))
    # print(type(rand_id))
    my_list=[11,22,33,44,55]
    query_set=Article.objects.all()

    context={
        "title":article_obj.title,
        "content":article_obj.content,
        "id":article_obj.id,
        "my_list":my_list,
        "object_list":query_set
    }

    # HTML_STRING="""
    # <h1>Hello {title}!.</h1>
    # <p1>{content} having id {id}.</p1>
    # """.format(**context)

    HTML_STRING=render_to_string("home-view.html",context=context)
    
    return HttpResponse(HTML_STRING)
