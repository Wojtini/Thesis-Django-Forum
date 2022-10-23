from django.template import loader

from Masquerade.settings import INDEX_CACHE
from forum import models
from forum.views.base_view import BaseView


class Index(BaseView):
    prerender_template = "index.html"
    cache_location = INDEX_CACHE

    def _get_prerender_view(self, *args, **kwargs):
        threads = sorted(models.Thread.objects.filter(indexed=True), key=lambda t: t.update_date, reverse=True)[0:3]
        return loader.render_to_string(
            self.prerender_template,
            context={
                "threads": threads,
            },
        )
