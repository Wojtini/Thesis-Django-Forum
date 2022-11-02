from django.template import loader

from forum import models
from forum.views.base_view import BaseView


class CategoryView(BaseView):
    prerender_template = "category.html"

    def _get_prerender_view(self, *args, **kwargs):
        category = models.Category.objects.get(name=kwargs.get("category_name"))
        return loader.render_to_string(
            self.prerender_template,
            context={
                "category": category,
                "threads": sorted(models.Thread.objects.filter(category=category), key=lambda t: t.update_date, reverse=True),
            },
        )
