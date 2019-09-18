from widgets.tests.mixins import TestDataMixin, random_string
from django.urls import reverse
from django.test import TestCase


class TestWidgetListView(TestDataMixin, TestCase):
    def setUp(self):
        # make 3 test widgets
        for _ in range(6):
            self.user2.widgets.create(name=random_string(128))

        self.url = reverse("widgets:index")
        self.response = self.client.get(self.url)

    def test_can_get_page(self):
        self.assertEqual(self.response.status_code, 200)

    def test_correct_template(self):
        self.assertTemplateUsed(self.response, "widgets/index.html")

    def test_pagination_is_five(self):
        context = self.response.context
        self.assertTrue(context["is_paginated"])
        self.assertEqual(context["is_paginated"], True)
        self.assertTrue(len(context["widgets"]), 5)

    def test_second_page(self):
        response = self.client.get("{}?page=2".format(reverse("widgets:index")))
        context = response.context
        self.assertTrue(context["is_paginated"])
        self.assertEqual(context["is_paginated"], True)
        self.assertTrue(len(context["widgets"]), 2)
