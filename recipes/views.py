from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from .forms import RecipeForm, RecipeIngredientForm
from .models import Recipe, RecipeIngredient
from django.forms.models import modelformset_factory
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
    obj = get_object_or_404(Recipe, id=id, user=request.user) 
    context = {
        "object": obj
    }
    return render(request, "recipes/detail.html", context) 



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
            if child.recipe is None:
                print("Added new")
                child.recipe = parent
            child.save()
        context['message'] = 'Data saved.'
    return render(request, "recipes/create-update.html", context)  