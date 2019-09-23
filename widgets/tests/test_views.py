from widgets.tests.mixins import TestDataMixin, random_string
from django.urls import reverse
from django.test import TestCase

from widgets.models import Comment


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


class TestWidgetDetailView(TestDataMixin, TestCase):
    def setUp(self):
        self.url = self.widget1.get_absolute_url()
        self.response = self.client.get(self.url)
    
    def test_correct_template(self):
        self.assertTemplateUsed(self.response, "widgets/detail.html")
    
    def test_anonymous_user_can_get(self):
        self.assertEquals(self.response.status_code, 200)
    
    def test_comment_button_not_in_template(self):
        self.assertNotContains(self.response, 'Add a Comment')
    
    def test_comment_button_in_template_authenticated_user(self):
        response = self.authenticated_client('testuser1', '12345').get(self.url)
        self.assertContains(response, 'Add a Comment')
    
    def test_comment_update_and_delete_buttons_for_commenter(self):
        response = self.authenticated_client('scrubby_mctroll', '12345').get(self.url)
        self.assertContains(response, '<i class="fa fa-trash"')
        self.assertContains(response, '<i class="fa fa-edit"')


class TestCommentCreateView(TestDataMixin, TestCase):
    def setUp(self):
        self.url = reverse('widgets:comment_create', kwargs={'pk': self.widget1.pk})
        self.client = self.authenticated_client('scrubby_mctroll', '12345')
    
    def test_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "widgets/comment_create.html")
    
    def test_form_submit_success_redirect(self):
        comment = random_string(128)
        response = self.client.post(self.url, data={'comment': comment})
        self.assertEqual(response.status_code, 302)
    
    def test_form_submit_success(self):
        comment = random_string(128)
        count_query = self.widget1.comments.count
        count = count_query()
        self.client.post(self.url, data={'comment': comment})
        self.assertEqual(count_query(), count + 1)

    def test_message_after_submit(self):
        comment = random_string(128)
        success_message = "The comment has been created."
        response = self.client.post(self.url, data={'comment': comment}, follow=True)
        messages = list(response.context['messages'])

        # test the html
        self.assertIn(success_message.encode('utf-8'), response.content)

        # test the messages iterable
        for message in messages:
            self.assertEqual(str(message), success_message)

    def test_form_submit_failure(self):
        response = self.client.post(self.url, data={'comment': random_string(1025)})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The comment is too long.")

    def test_form_submit_failure_no_input(self):
        response = self.client.post(self.url, data={'comment': ''})
        self.assertEqual(response.status_code, 200)


class TestCommentUpdateView(TestDataMixin, TestCase):
    def setUp(self):
        self.comment = self.widget1.comments.create(user=self.commenter, comment=random_string(125))
        self.url = reverse('widgets:comment_update', kwargs={'pk': self.comment.pk})
        self.post_client = self.authenticated_client('scrubby_mctroll', '12345')
    
    def test_correct_template(self):
        response = self.post_client.get(self.url)
        self.assertTemplateUsed(response, "widgets/comment_update.html")
    
    def test_anonymous_cannot_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
    
    def test_other_user_cannot_get(self):
        guest_client = self.authenticated_client('testuser1', '12345')
        response = guest_client.get(self.url)
        self.assertEqual(response.status_code, 403)
    
    def test_anonymous_cannot_post(self):
        response = self.client.post(self.url, data={'comment': random_string(125)})
        self.assertEqual(response.status_code, 403)
    
    def test_other_user_cannot_post(self):
        guest_client = self.authenticated_client('testuser1', '12345')
        response = guest_client.post(self.url, data={'comment': random_string(125)})
        self.assertEqual(response.status_code, 403)
    
    def test_form_submit_success_redirect(self):
        comment = random_string(128)
        response = self.post_client.post(self.url, data={'comment': comment})
        self.assertEqual(response.status_code, 302)
    
    def test_form_submit_success(self):
        comment = random_string(128)
        self.post_client.post(self.url, data={'comment': comment})
        self.assertEqual(self.widget1.comments.get(pk=self.comment.pk).comment, comment)

    def test_message_after_submit(self):
        comment = random_string(128)
        success_message = "The comment has been updated."
        response = self.post_client.post(self.url, data={'comment': comment}, follow=True)
        messages = list(response.context['messages'])

        # test the html
        self.assertIn(success_message.encode('utf-8'), response.content)

        # test the messages iterable
        for message in messages:
            self.assertEqual(str(message), success_message)

    def test_form_submit_failure(self):
        response = self.post_client.post(self.url, data={'comment': random_string(1025)})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The comment is too long.")

    def test_form_submit_failure_no_input(self):
        response = self.post_client.post(self.url, data={'comment': ''})
        self.assertEqual(response.status_code, 200)


class TestCommentDeleteView(TestDataMixin, TestCase):
    def setUp(self):
        self.comment = self.widget1.comments.create(user=self.commenter, comment=random_string(125))
        self.url = reverse('widgets:comment_delete', kwargs={'pk': self.comment.pk})
        self.post_client = self.authenticated_client('scrubby_mctroll', '12345')
    
    def test_correct_template(self):
        response = self.post_client.get(self.url)
        self.assertTemplateUsed(response, "widgets/comment_delete.html")
    
    def test_anonymous_cannot_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
    
    def test_other_user_cannot_get(self):
        guest_client = self.authenticated_client('testuser1', '12345')
        response = guest_client.get(self.url)
        self.assertEqual(response.status_code, 403)
    
    def test_anonymous_cannot_post(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, 403)
    
    def test_other_user_cannot_post(self):
        guest_client = self.authenticated_client('testuser1', '12345')
        response = guest_client.post(self.url, data={})
        self.assertEqual(response.status_code, 403)
    
    def test_form_submit_success_redirect(self):
        response = self.post_client.post(self.url, data={})
        self.assertEqual(response.status_code, 302)
    
    def test_form_submit_success(self):
        count_query = self.widget1.comments.count
        count = count_query()
        self.post_client.post(self.url, data={})
        self.assertEqual(count_query(), count - 1)

    def test_message_after_submit(self):
        comment = random_string(128)
        success_message = "The comment has been deleted."
        response = self.post_client.post(self.url, data={'comment': comment}, follow=True)
        messages = list(response.context['messages'])

        # test the html
        self.assertIn(success_message.encode('utf-8'), response.content)

        # test the messages iterable
        for message in messages:
            self.assertEqual(str(message), success_message)
