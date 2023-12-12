from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError


class UserTest(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        email = 'test@example.com'
        password = 'testpassword'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email)
            self.assertEqual(user.email, expected)

    def test_duplicate_entry_raises_error(self):
        """Test duplicate email entry raises an error"""
        get_user_model().objects.create_user('test@example.com')
        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user('test@example.com')

    def test_new_user_without_email_raises_error(self):
        """Test creating a user without an email raises an error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
