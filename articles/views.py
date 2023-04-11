from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# Create your views here.

from .models import Article
from .forms import ArticleForm
from .forms import ArticleFormNew


def article_detail_view(request, id=None):
    article_obj = None
    if id is not None:
        article_obj = Article.objects.get(id=id)
    context = {
        "object": article_obj
    }
    return render(request, 'articles/detail.html', context=context)


def article_search_view(request):

    print(request.GET)
    query_dict = request.GET  # GET REQUEST CONSISTS OF DICTIONARY

    # query=query_dict.get('q') #HERE WE FETCH THE VALUE OF 'q' from the GET REQUEST DICTIONARY{'q':ENTERED INT} , <input type="text" name="q">

    try:
        query = int(query_dict.get('q'))
    except:
        query = None

    article_obj = None
    if query is not None:
        article_obj = Article.objects.get(id=query)

    context = {
        "object": article_obj
    }
    return render(request, 'articles/search.html', context=context)

# for the sake of simple create article
# @login_required
# def article_create_view (request):

#     ''' agar user login nhi h to pehle ye login krne ke liye bolega
#      if not request.user.is_authenticated:
#          return redirect('/login') '''

#     context={
#     }
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         content=request.POST.get('content')
#         print(title,content)
#         article_object = Article.objects.create(title=title,content=content)

#         context['object']=article_object
#         context['created']=True


#     return render(request,'articles/create.html',context=context)

# for the sake of handling repetitive creation of articles
# @login_required
# def article_create_view(request):
#     ''' agar user login nhi h to pehle ye login krne ke liye bolega
#      if not request.user.is_authenticated:
#          return redirect('/login') '''

#     form = ArticleForm() # for the sake of GET requests initially
#     context = {
#         'form': form
#     }
#     if request.method == 'POST':
#         form = ArticleForm(request.POST)
#         context['form'] = form
#         if form.is_valid():
#           title = form.cleaned_data.get('title')
#           content = form.cleaned_data.get('content')
#           article_object = Article.objects.create(title=title, content=content)
#           context['object'] = article_object
#           context['created'] = True
#     return render(request, 'articles/create.html', context=context)

# for class ArticleForm
# @login_required
# def article_create_view(request):
#     ''' agar user login nhi h to pehle ye login krne ke liye bolega
#      if not request.user.is_authenticated:
#          return redirect('/login') '''

#     form = ArticleForm(request.POST or None) # for the sake of GET requests initially for NONE
#     context = {
#         'form': form
#     }
#     if form.is_valid(): # valid ka matlab posted data duplcated nhi h
#         title = form.cleaned_data.get('title')
#         content = form.cleaned_data.get('content')
#         #ALSO
#         # title = request.POST.get('title')
#         # content=request.POST.get('content')
#         article_object = Article.objects.create(title=title, content=content)
#         context['object'] = article_object
#         context['created'] = True
#     return render(request, 'articles/create.html', context=context)

# for class ArticleFormNew
@login_required
def article_create_view(request):
    ''' agar user login nhi h to pehle ye login krne ke liye bolega
     if not request.user.is_authenticated:
         return redirect('/login') '''

    form = ArticleFormNew(request.POST or None) # for the sake of GET requests initially for NONE
    context = {
        'form': form
    }
    if form.is_valid(): # valid ka matlab posted data duplcated nhi h
        article_object = form.save() #agar valid ho to seedhe post request pe hi create ho jayega object,phir save kr liye
        # ye sab bkchodi krne ki zarrorat nhi hai,agar valid ho to seedhe post request pe hi create ho jayega object,phir upar save kr liye
        # title = form.cleaned_data.get('title')
        # content = form.cleaned_data.get('content')
        # article_object = Article.objects.create(title=title, content=content)
        context['object'] = article_object
        context['created'] = True
    return render(request, 'articles/create.html', context=context)
