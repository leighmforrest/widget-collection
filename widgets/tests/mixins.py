import string
import random

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import Client


def random_string(string_length=10):
    """Helper to generate dummy data"""
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(string_length))


class TestDataMixin:
    @classmethod
    def setUpTestData(cls):
        """Set up basic immutable data for the test."""
        cls.user1 = get_user_model().objects.create_user(
            username="testuser1", password="12345"
        )
        cls.user2 = get_user_model().objects.create_user(
            username="testuser2", password="12345"
        )
        cls.commenter = get_user_model().objects.create_user(
            username="scrubby_mctroll", password="12345"
        )

        # add permissions to users 1 and 2
        permission = Permission.objects.get(codename="curator")
        cls.user1.user_permissions.add(permission)
        cls.user2.user_permissions.add(permission)

        # create widgets
        cls.widget1 = cls.user1.widgets.create(name=random_string(256))
        cls.max_widget = cls.user2.widgets.create(name=random_string(256))

        # add 6 notes to max
        for _ in range(6):
            cls.max_widget.notes.create(text=random_string(128))

        # add comments
        cls.commenter.comments.create(
            comment=random_string(512), widget=cls.widget1)

    def authenticated_client(self, username, password):
        """Helper to build an authenticated client for tests."""
        client = Client()
        client.login(username=username, password=password)
        return client
