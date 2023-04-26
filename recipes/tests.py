from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError

# Create your tests here.
from .models import RecipeIngredient, Recipe

User = get_user_model()


class UserTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user('cfe', password='abc123')

    def test_user_pw(self):
        checked = self.user_a.check_password("abc123")
        self.assertTrue(checked)


class RecipeTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user('cfe', password='abc123')
        self.recipe_a = Recipe.objects.create(
            name='Grilled Chicken',
            user=self.user_a
        )
        self.recipe_b = Recipe.objects.create(
            name='Grilled Chicken Tacos',
            user=self.user_a
        )
        self.recipe_ingredient_a = RecipeIngredient.objects.create(
            recipe=self.recipe_a,
            name='Chicken',
            quantity='1/2',
            unit='pound'
        )
        self.recipe_ingredient_b = RecipeIngredient.objects.create(
            recipe=self.recipe_a,
            name='Chicken',
            quantity='asdfasd',
            unit='pound'
        )

    def test_user_count(self):
        qs = User.objects.all()
        self.assertEqual(qs.count(), 1)

    def test_user_recipe_reverse_count(self):
        user = self.user_a
        qs = user.recipe_set.all()  # user ke andar ki recipes se connect ke diya
        self.assertEqual(qs.count(), 2)

    def test_user_recipe_forward_count(self):
        user = self.user_a
        # recipes ke andar ke user(foreign key)  se connect ke diya
        qs = Recipe.objects.filter(user=user)
        self.assertEqual(qs.count(), 2)

    def test_recipe_ingredient_reverse_count(self):
        recipe = self.recipe_a
        qs = recipe.recipeingredient_set.all()
        self.assertEqual(qs.count(), 2)

    def test_recipe_ingredientcount(self):
        recipe = self.recipe_a
        qs = RecipeIngredient.objects.filter(recipe=recipe)
        self.assertEqual(qs.count(), 2)

    def test_user_two_level_relation(self):
        user = self.user_a
        qs = RecipeIngredient.objects.filter(recipe__user=user)
        self.assertEqual(qs.count(), 2)

    def test_user_two_level_relation_reverse(self):
        user = self.user_a
        recipeingredient_ids = list(user.recipe_set.all(
        ).values_list('recipeingredient__id', flat=True))
        qs = RecipeIngredient.objects.filter(id__in=recipeingredient_ids)
        self.assertEqual(qs.count(), 2)

    def test_user_two_level_relation_via_recipes(self):
        user = self.user_a
        ids = user.recipe_set.all().values_list("id", flat=True)
        qs = RecipeIngredient.objects.filter(recipe__id__in=ids)
        self.assertEqual(qs.count(), 2)

    def test_unit_measure_validation(self):
        valid_unit = 'ounce'
        ingredient = RecipeIngredient(
            recipe=self.recipe_a,
            name='New',
            quantity=10,
            unit=valid_unit
        )
        ingredient.full_clean()

    def test_unit_measure_validation_error(self):
        invalid_units = ['nada', 'asdfadsf']
        with self.assertRaises(ValidationError):
            for unit in invalid_units:
                ingredient = RecipeIngredient(
                    recipe=self.recipe_a,
                    name='New',
                    quantity=10,
                    unit=unit
                )
                ingredient.full_clean()

    def test_quantity_as_float(self):
        self.assertIsNotNone(self.recipe_ingredient_a.quantity_as_float) #valid value hai isiliye quantity_as_float field none nhi hoga,so passed
        self.assertIsNone(self.recipe_ingredient_b.quantity_as_float) #valid value hai isiliye quantity_as_float field none hoga,so passed
