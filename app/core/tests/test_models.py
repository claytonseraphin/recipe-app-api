from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email="clayton0687@gmail.com", password="test123"):
    """Create a sample user."""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_succesful(self):
        """ Test creating a new user with an email is succesful"""
        email = "clayton@bawonevent.com"
        password = "password123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = "clayton@BAWONEVENT.com"
        user = get_user_model().objects.create_user(email, 'pass123')

        self.assertEqual(user.email, email.lower())

    def test_email_field_is_required(self):
        """Raise error when a new user doesn't provide an email address"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_super_user(self):
        """ Test to create a new super user with email and password"""
        user = get_user_model().objects.create_superuser(
            'test@gmail.com',
            'test123'
            )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation."""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name="Vegan"
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_string(self):
        """Test the ingredient string representation."""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name="Hot Sauce"
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_reciper_string(self):
        """Test the recipe string representation."""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title="Diri Blan Sos Pwa legim",
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)
