from contextlib import suppress

from django.test import TestCase
from django.contrib.auth import get_user_model


class UserManagerTests(TestCase):

    def test_create_user(self):
        ZetUser = get_user_model()
        user = ZetUser.objects.create_user(
            username='test_user',
            password='awesome_password'
        )
        self.assertEqual(user.username, 'test_user')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        with suppress(AttributeError):
            self.assertIsNone(user.email)

        with self.assertRaises(TypeError):
            ZetUser.objects.create_user()

        with self.assertRaises(TypeError):
            ZetUser.objects.create_user(username='')

        with self.assertRaises(TypeError):
            ZetUser.objects.create_user(username='abc')

        with self.assertRaises(ValueError):
            ZetUser.objects.create_user(username='', password='awesome_password')

    def test_create_superuser(self):
        ZetUser = get_user_model()
        superuser = ZetUser.objects.create_superuser(
            username='test_superuser',
            password='super_password'
        )
        self.assertEqual(superuser.username, 'test_superuser')
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)








