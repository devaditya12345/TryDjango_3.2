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
    if not request.htmx:
        raise Http404
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
    #Commenting for making forms more dynamic using htmx , in the 68th video (edit wala)
    # RecipeIngredientFormset = modelformset_factory(RecipeIngredient, form=RecipeIngredientForm, extra=0)
    # qs = obj.recipeingredient_set.all() # []
    # formset = RecipeIngredientFormset(request.POST or None, queryset=qs)
    
    new_ingredient_url = reverse("recipes:hx-ingredient-create", kwargs={"parent_id": obj.id})
    context = {
        "form": form,
        # "form_2": form_2,
        # "formset": formset,
        "object": obj,
        "new_ingredient_url": new_ingredient_url
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


#isliye comment kiye kyonki 68th video me formset hta diye the to yha pe uski validity check nhi krna tha
    # if all([form.is_valid(), formset.is_valid()]):
    #     parent = form.save(commit=False)
    #     parent.save()
        
    #     # formset.save()
    #     for form in formset:
    #         child = form.save(commit=False)
    #         child.recipe = parent
    #         child.save()
    if form.is_valid():
        form.save()
        context['message'] = 'Data saved.'
    if request.htmx: # YE IMP HAI ACCHE SE PADHO(Add more pe click krne se ek new recipe ingredient form add hoga, phir jb hm usko fill kr ke save karenge tab hx-post='.' trigger hogi (save hi yha par htmx trigger ka kaam karega) aur save hoga(shayad javascript ka involvement isme nhi hoga not sure) and recent_update_view render hoga , bs isiliye forms.html pe bhej rhe h,jiske base.html ka content repeat na ho)
        return render(request,"recipes/partials/forms.html",context)
    return render(request, "recipes/create-update.html", context)  

@login_required
def recipe_ingredient_update_hx_view(request, parent_id=None, id=None):
    if not request.htmx:
        raise Http404
    try:
        parent_obj = Recipe.objects.get(id=parent_id, user=request.user)
    except:
        parent_obj = None
    if parent_obj is  None:
        return HttpResponse("Not found.")
    instance = None
    if id is not None:
        try:
            instance = RecipeIngredient.objects.get(recipe=parent_obj, id=id)
        except:
            instance = None
    form = RecipeIngredientForm(request.POST or None, instance=instance)
    url = reverse("recipes:hx-ingredient-create", kwargs={"parent_id": parent_obj.id})
    if instance:
        url = instance.get_hx_edit_url()
    context = {
        "url": url,
        "form": form,
        "object": instance
    }
    if form.is_valid():
        new_obj = form.save(commit=False)
        if instance is None:
            new_obj.recipe = parent_obj
        new_obj.save()
        context['object'] = new_obj
        return render(request, "recipes/partials/ingredient-inline.html", context) 
    return render(request, "recipes/partials/ingredient-form.html", context) 