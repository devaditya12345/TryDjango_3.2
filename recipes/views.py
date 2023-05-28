from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from .forms import RecipeForm, RecipeIngredientForm, RecipeIngredientImageForm
from .models import Recipe, RecipeIngredient
from django.forms.models import modelformset_factory
from django.urls import reverse
from django.http import HttpResponse, Http404
from .services import extract_text_via_ocr_service
from .utils import (
    convert_to_qty_units,
    parse_paragraph_to_recipe_line
)
import json
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


# Commenting for the sake of htmx
# @login_required
# def recipe_delete_view(request, id=None):
#     obj = get_object_or_404(Recipe, id=id, user=request.user)
#     if request.method == "POST":
#         obj.delete()
#         success_url = reverse('recipes:list')
#         return redirect(success_url)
#     context = {
#         "object": obj
#     }
#     return render(request, "recipes/delete.html", context)


# Commenting for the sake of htmx
# @login_required
# def recipe_incredient_delete_view(request, parent_id=None, id=None):
#     obj = get_object_or_404(RecipeIngredient, recipe__id=parent_id, id=id, recipe__user=request.user)
#     if request.method == "POST":
#         obj.delete()
#         success_url = reverse('recipes:detail', kwargs={"id": parent_id})
#         return redirect(success_url)
#     context = {
#         "object": obj
#     }
#     return render(request, "recipes/delete.html", context)

# htmx
@login_required
def recipe_delete_view(request, id=None):
    try:
        obj = Recipe.objects.get(id=id, user=request.user)
    except:
        obj = None
    if obj is None:
        if request.htmx:
            return HttpResponse("Not Found")
        raise Http404
    if request.method == "POST":
        obj.delete()
        success_url = reverse('recipes:list')
        if request.htmx:
            headers = {
                'HX-Redirect': success_url
            }
            return HttpResponse("Success", headers=headers)
        return redirect(success_url)
    context = {
        "object": obj
    }
    return render(request, "recipes/delete.html", context)

# htmx
@login_required
def recipe_incredient_delete_view(request, parent_id=None, id=None):
    obj = get_object_or_404(RecipeIngredient, recipe__id=parent_id, id=id, recipe__user=request.user)
    try:
        obj = RecipeIngredient.objects.get(recipe__id=parent_id, id=id, recipe__user=request.user)
    except:
        obj = None
    if obj is None:
        if request.htmx:
            return HttpResponse("Not Found")
        raise Http404
    if request.method == "POST":
        name = obj.name
        obj.delete()
        success_url = reverse('recipes:detail', kwargs={"id": parent_id})
        if request.htmx:
            return render(request, "recipes/partials/ingredient-inline-delete-response.html", {"name": name})
        return redirect(success_url)
    context = {
        "object": obj
    }
    return render(request, "recipes/delete.html", context)

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

        if request.htmx:
            headers = {
                "HX-Redirect": obj.get_absolute_url()
            }
            return HttpResponse("Created", headers=headers)
        
            # DIRECT /partials/detail.html ME BHI JAAKER BHI SAKTA HAI
            # context = {
            #     "object": obj
            # }
            #return render(request, "recipes/partials/detail.html", context)
        return redirect(obj.get_absolute_url()) #it's working without it.After handling with htmx and also we don't need request.htmx after using this.
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
    if form.is_valid(): #mere khayal se tabhi call hoga jb form ke andar kuch likh kr usko save karenge, tb message show hoenga.
        form.save()
        context['message'] = 'Data saved.'
    if request.htmx: # YE IMP HAI ACCHE SE PADHO(Add more pe click krne se ek new recipe ingredient form add hoga, phir jb hm usko fill kr ke save karenge tab hx-post='.' trigger hogi (save hi yha par htmx trigger ka kaam karega) aur save hoga(shayad javascript ka involvement isme nhi hoga not sure) and recent_update_view render hoga , bs isiliye forms.html pe bhej rhe h,jiske base.html ka content repeat na ho)
        return render(request,"recipes/partials/forms.html",context)
    return render(request, "recipes/create-update.html", context)  


# edit ka use krte waqt hmne yha pe mast url ka use kiya hai,without going to any actual path
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

# Commented to implement the htmx below
# @login_required
# def recipe_ingredient_image_upload_view(request, parent_id=None):
#     try:
#         parent_obj = Recipe.objects.get(id=parent_id, user=request.user)
#     except:
#         parent_obj = None
#     if parent_obj is None:
#         raise Http404
#     form = RecipeIngredientImageForm(request.POST or None, request.FILES or None)
#     if form.is_valid():
#         obj = form.save(commit=False)
#         obj.recipe = parent_obj
#         # obj.recipe_id = parent_id
#         obj.save()
#     return render(request, "image-form.html", {"form":form})

def recipe_ingredient_image_upload_view(request, parent_id=None):
    template_name = "recipes/upload-image.html"
    if request.htmx:
        template_name = "recipes/partials/image-upload-form.html"
    try:
        parent_obj = Recipe.objects.get(id=parent_id, user=request.user)
    except:
        parent_obj = None
    if parent_obj is None:
        raise Http404
    form = RecipeIngredientImageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.recipe = parent_obj
        # obj.recipe_id = parent_id
        obj.save()

         # send image file -> microservice api
        # microservice api -> data about the file
        # cloud providers $$

        # result = extract_text_via_ocr_service(obj.image)
        # obj.extracted = result
        extracted = extract_text_via_ocr_service(obj.image)
        obj.extracted = extracted
        obj.save()
        # print(obj.extracted)

        parsed_data = json.loads(extracted)
        og = parsed_data['ParsedResults'][0]['ParsedText']

        # og = extracted['parsed_text']
        results = parse_paragraph_to_recipe_line(og)
        dataset = convert_to_qty_units(results)
        new_objs = []
        for data in dataset:
            data['recipe_id']  = parent_id
            new_objs.append(RecipeIngredient(**data))
        RecipeIngredient.objects.bulk_create(new_objs)
        success_url = parent_obj.get_edit_url()
        if request.htmx:
            headers = {
                'HX-Redirect': success_url
            }
            return HttpResponse("Success", headers=headers)
        return redirect(success_url)
    return render(request, template_name, {"form":form})