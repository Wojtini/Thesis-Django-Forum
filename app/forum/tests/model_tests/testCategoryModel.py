from django.test import TestCase

from forum.models import Category, Thread


class CategoryModelTests(TestCase):
    def setUp(self) -> None:
        Category.objects.create(name="Category_Empty")
        category = Category.objects.create(name="Category_with_threads")
        Thread.objects.create(title="Thread_1", category=category)
        Thread.objects.create(title="Thread_2", category=category)
        Thread.objects.create(title="Thread_3", category=None)

    def test_empty_category(self):
        cat = Category.objects.get(name="Category_Empty")
        self.assertTrue(cat.is_empty)

    def test_category_with_threads(self):
        cat = Category.objects.get(name="Category_with_threads")
        self.assertTrue(cat.number_of_active_threads == 2)
