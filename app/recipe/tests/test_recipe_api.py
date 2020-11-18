from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from core.models import Recipe

from recipe.serializers import RecipeSerializer

from rest_framework import status
from rest_framework.test import APIClient

RECIPE_URL = reverse('recipe:recipe-list')


def sample_recipe(user, **params):
    """Create and return a samle recipe."""
    defaults = {
        'title': 'sample recipe',
        'time_minutes': 10,
        'price': 7.00,
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeApiTest(TestCase):
    """Test the publicly available recipe endpoint."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication required to access the recipe endpoint."""
        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):
    """Test authenticated API access."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'lolo@gmail.com',
            'testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving list of recipes"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """Test only recipes for authenticated user are returned."""
        user2 = get_user_model().objects.create_user(
            'test@gmail.com',
            'pass123'
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    """
    def test_create_recipe_succesful(self):
        # Test the recipe is created succesfully.
        payload = Recipe.objects.create(
            user = self.user,
            title="Diri Kole",
            time_minutes=10,
            price=100.00
        )
            self.client.post(RECIPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
    """
