from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from .forms import RecipeForm, RecipeIngredientForm
from .models import Recipe, RecipeIngredient
from django.forms.models import modelformset_factory
from django.urls import reverse
from django.http import HttpResponse, Http404
# CRUD -> Create Retrieve Update & Delete

@login_required
def recipe_list_view(request):
    qs = Recipe.objects.filter(user=request.user)
    context = {
        "object_list": qs
    }
    return render(request, "recipes/list.html", context)


@login_required
def recipe_detail_view(request, id=None):
    # obj = get_object_or_404(Recipe, id=id, user=request.user) 
    hx_url = reverse("recipes:hx-detail", kwargs={"id": id})
    context = {
        # "object": obj
        "hx_url": hx_url
    }
    return render(request, "recipes/detail.html", context) 

@login_required
def recipe_detail_hx_view(request, id=None):
    try:
        obj = Recipe.objects.get(id=id, user=request.user)
    except:
        obj = None
    if obj is  None:
        return HttpResponse("Not found.")
    context = {
        "object": obj
    }
    return render(request, "recipes/partials/detail.html", context) 



@login_required
def recipe_create_view(request):
    form = RecipeForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False) # iska matlab
        obj.user = request.user
        obj.save()
        return redirect(obj.get_absolute_url())
    return render(request, "recipes/create-update.html", context)  

@login_required
def recipe_update_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=obj)
    # form_2 = RecipeIngredientForm(request.POST or None)

    # Formset = modelformset_factory(Model, form=ModelForm, extra=0)
    RecipeIngredientFormset = modelformset_factory(RecipeIngredient, form=RecipeIngredientForm, extra=0)
    qs = obj.recipeingredient_set.all() # []
    formset = RecipeIngredientFormset(request.POST or None, queryset=qs)
    context = {
        "form": form,
        # "form_2": form_2,
        "formset": formset,
        "object": obj
    }
    # if form.is_valid(): PEHLE 
    #     form.save() 

    # if all([form.is_valid(), form_2.is_valid()]): 2ND TIME
    #     parent = form.save(commit=False)
    #     parent.save()
    #     child = form_2.save(commit=False)
    #     child.recipe = parent # IISE PARENT RECIPE (MAINLY NAME ME  CURRENT RECEPEINGREDIENTS  WALE KA NAME AA JA RHA HAI) KYU ????
    #     #BUT JAB HM DIRECT ADMIN PANEL ME EK NEW RECIPE INGREDIENT ADD KRKR USKI NAMING KR RHE HAI TO HMARE PARENT NAME OF RECIPE PE KOI AFFECT NHI AA RHA HAI
    #     child.save()
    #     print("form", form.cleaned_data)
    #     print("form_2", form_2.cleaned_data)
    #     context['message'] = 'Data saved.'
    # return render(request, "recipes/create-update.html", context)  

    if all([form.is_valid(), formset.is_valid()]):
        parent = form.save(commit=False)
        parent.save()
        
        # formset.save()
        for form in formset:
            child = form.save(commit=False)
            child.recipe = parent
            child.save()
        context['message'] = 'Data saved.'
        if request.htmx: # YE IMP HAI ACCHE SE PADHO(Add more pe click krne se ek new recipe ingredient form add hoga, phir jb hm usko fill kr ke save karenge tab hx-post='.' trigger hogi (save hi yha par htmx trigger ka kaam karega) aur save hoga(shayad javascript ka involvement isme nhi hoga not sure) and recent_update_view render hoga , bs isiliye forms.html pe bhej rhe h,jiske base.html ka content repeat na ho)
            return render(request,"recipes/partials/forms.html",context)
    return render(request, "recipes/create-update.html", context)  