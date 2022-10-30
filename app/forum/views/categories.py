from django.template import loader

from forum.forms import CategoryForm
from forum.models import Category
from forum.views.base_view import BaseView


class CategoryListView(BaseView):
    prerender_template = "categories_list.html"
    form_class = CategoryForm

    def _get_prerender_view(self, *args, **kwargs):
        return loader.render_to_string(
            self.prerender_template,
            context={
                "categories": Category.objects.all(),
            }
        )
