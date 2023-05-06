from django.conf import settings
from django.db import models
from .validators import validate_unit_of_measure
from .utils import number_str_to_float
import pint  #pint is having problems such as invalid conversions such as litres to metres(in mks) and to yards(in imperial).
from django.urls import reverse

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

#Parent class
class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    active = models.BooleanField(default=True)

    def get_absolute_url(self): # hai to reverse url hi
        # return "/pantry/recipes/"
        return reverse("recipes:detail", kwargs={"id": self.id})
    
    def get_edit_url(self):
        return reverse("recipes:update", kwargs={"id": self.id})

    def get_hx_url(self):
        return reverse("recipes:hx-detail", kwargs={"id": self.id})
   
    def get_ingredients_children(self):
        return self.recipeingredient_set.all()

#Considered as a child class of Recipe Class connected by foreign key
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    quantity = models.CharField(max_length=50)  # 1 1/4
    # pounds, lbs, oz, gram, etc
    quantity_as_float = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=50, validators=[validate_unit_of_measure]) 
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return self.recipe.get_absolute_url()

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
        measurement = self.quantity_as_float * ureg[self.unit] #float value * ureg(jisme change krni h) to [self.unit](jiise chage krni h)
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