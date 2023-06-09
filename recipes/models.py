import pint  #pint is having problems such as invalid conversions such as litres to metres(in mks) and to yards(in imperial).
import pathlib
import uuid


from django.conf import settings
from django.db import models
from .validators import validate_unit_of_measure
from .utils import number_str_to_float

from django.urls import reverse
from django.db.models import Q

"""
- Global
    - Ingredients
    - Recipes
- User
    - Ingredients
    - Recipes
        - Ingredients
        - Directions for Ingredients
"""

class RecipeQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.none()
        lookups = (
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(directions__icontains=query)
        )
        return self.filter(lookups) 

class RecipeManager(models.Manager):
    def get_queryset(self):
        return RecipeQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)
    


#Parent class
class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    active = models.BooleanField(default=True)


    objects = RecipeManager()

    @property
    def title(self):
        return self.name #agar khi pe recipe.title call hua to wha name jayega

    def get_absolute_url(self): # hai to reverse url hi
        # return "/pantry/recipes/"
        return reverse("recipes:detail", kwargs={"id": self.id})
    
    def get_edit_url(self):
        return reverse("recipes:update", kwargs={"id": self.id})

    def get_hx_url(self):
        return reverse("recipes:hx-detail", kwargs={"id": self.id})
    
    def get_delete_url(self):
        return reverse("recipes:delete", kwargs={"id": self.id})
   
    def get_ingredients_children(self):
        return self.recipeingredient_set.all()
    
    # def get_upload_url(self): 
    #     return reverse("recipes:image-upload", kwargs={"parent_id": self.id})
    
    def get_image_upload_url(self):
        return reverse("recipes:recipe-ingredient-image-upload", kwargs={"parent_id": self.id})


def recipe_ingredient_image_upload_handler(instance, filename):
    fpath = pathlib.Path(filename)
    new_fname = str(uuid.uuid1()) # uuid1 -> uuid + timestamps
    return f"recipes/ingredient/{new_fname}{fpath.suffix}"


class RecipeIngredientImage(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    # recipe_id = models.AutoField -> ID to Recipe
    image = models.ImageField(upload_to=recipe_ingredient_image_upload_handler) # path/to/the/actual/file.png
    extracted = models.TextField(blank=True, null=True)
    # image
    # extracted_text

   

#Considered as a child class of Recipe Class connected by foreign key
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    quantity = models.CharField(max_length=50, blank=True, null=True)  # 1 1/4
    # pounds, lbs, oz, gram, etc
    quantity_as_float = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=50, validators=[validate_unit_of_measure], blank=True, null=True) 
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return self.recipe.get_absolute_url()
    
    def get_delete_url(self):
        kwargs = {
            "parent_id": self.recipe.id,
            "id": self.id
        }
        return reverse("recipes:ingredient-delete", kwargs=kwargs)

    def get_hx_edit_url(self):
        kwargs = {
            "parent_id": self.recipe.id,
            "id": self.id
        }
        return reverse("recipes:hx-ingredient-detail", kwargs=kwargs)

    def convert_to_system(self, system="mks"):
        if self.quantity_as_float is None:
            return None
        ureg = pint.UnitRegistry(system=system)
        measurement = self.quantity_as_float * ureg[self.unit.lower()] #float value * ureg(jisme change krni h) to [self.unit](jiise chage krni h)
        return measurement #.to_base_units()

    def as_mks(self):
        # meter, kilogram, second
        measurement = self.convert_to_system(system='mks')
        return measurement.to_base_units()

    def as_imperial(self):
        # miles, pounds, seconds
        measurement = self.convert_to_system(system='imperial')
        return measurement.to_base_units()

    def save(self, *args, **kwargs):
        qty = self.quantity
        qty_as_float, qty_as_float_success = number_str_to_float(qty)
        if qty_as_float_success:
            self.quantity_as_float = qty_as_float
        else:
            self.quantity_as_float = None
        super().save(*args, **kwargs)


# class RecipeImage():
#     recipe = models.ForeignKey(Recipe)