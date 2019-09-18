from widgets.tests.mixins import TestDataMixin, random_string
from widgets.models import Comment
from django.test import TestCase


class TestWidget(TestDataMixin, TestCase):
    def test_widget_exists(self):
        self.assertIsNotNone(self.widget1)

    def test_widget_fields(self):
        widget = self.widget1
        self.assertEqual(widget.pk, self.widget1.pk)
        self.assertEqual(widget.name, self.widget1.name)
        self.assertIsNotNone(widget.created_at)
        self.assertIsNotNone(widget.updated_at)

    def test_string(self):
        self.assertEqual(self.widget1.name, str(self.widget1))

    def test_create_widget(self):
        name = random_string(256)
        widget = self.user1.widgets.create(name=name)
        self.assertIsNotNone(widget)
        self.assertEqual(widget.name, name)

    def test_asbolute_url(self):
        pass


class TestComment(TestDataMixin, TestCase):
    def setUp(self):
        self.test_comment = self.widget1.comments.create(
            user=self.commenter, comment=random_string(1024)
        )

    def test_comment_exists(self):
        self.assertIsNotNone(self.test_comment.comment)

    def test_create_comment(self):
        comment_text = random_string(1024)
        comment = self.widget1.comments.create(
            user=self.commenter, comment=comment_text
        )
        self.assertEqual(comment.widget.pk, self.widget1.pk)
        self.assertEqual(comment.comment, comment_text)

    def test_valid_fields(self):
        comment = Comment.objects.get(pk=self.test_comment.pk)
        self.assertEqual(self.test_comment, comment)
        self.assertEqual(comment.user, self.commenter)

    def test_long_string(self):
        content = random_string(76)
        self.test_comment.comment = content
        self.assertEqual(content[:75] + "...", str(self.test_comment))

    def test_short_string(self):
        content = random_string(15)
        self.test_comment.comment = content
        self.assertEqual(content, str(self.test_comment))
