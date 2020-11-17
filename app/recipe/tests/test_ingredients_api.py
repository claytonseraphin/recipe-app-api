from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from core.models import Ingredient
from recipe.serializers import IngredientSerializer

from rest_framework import status
from rest_framework.test import APIClient


INGREDIENT_URL = reverse('recipe:ingredient-list')


class PublicIngredientApiTest(TestCase):
    """Test the publicly available API."""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test the user is logged in to access the ingredient endpoint."""
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientAPITest(TestCase):
    """ Test the authorized user ingredient API."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'clayton@gmail.com',
            'testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)


    def test_retrieve_ingredients(self):
        """Test retrievng ingredients."""
        Ingredient.objects.create(
            user=self.user,
            name='Vinegar'
        )

        Ingredient.objects.create(
            user=self.user,
            name="Salt"
        )

        res = self.client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that only ingredients for authenticated user are returned."""
        user2 = get_user_model().objects.create_user(
            'loko@gmail.com',
            'testpass'
        )
        Ingredient.objects.create(user=user2, name="Onion")

        ingredient = Ingredient.objects.create(user=self.user, name='Pasta')

        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient_succesful(self):
        """ Test a new ingredient is created succesfully."""
        payload = {'name': 'Carrot'}
        self.client.post(INGREDIENT_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_ingredient_with_invalid_credential(self):
        """ Test creating invalid ingredient fails."""
        payload = {'name': ''}
        res = self.client.post(INGREDIENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
