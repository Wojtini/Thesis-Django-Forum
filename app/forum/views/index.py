from django.db.models import Max
from django.template import loader

from forum.models import Thread
from forum.views.base_view import BaseView


class IndexView(BaseView):
    prerender_template = "index.html"
    cache_location = None

    def _get_prerender_view(self, *args, **kwargs):
        threads = Thread.objects.annotate(pop_max=Max("cyclethread__popularity")).order_by("-pop_max")
        if len(threads) == 0:
            return loader.render_to_string(
                self.prerender_template,
                context={
                    "header": "The forum is empty",
                },
            )
        most_popular_threads = threads.exclude(pop_max=None)
        if len(most_popular_threads) == 0:
            return loader.render_to_string(
                self.prerender_template,
                context={
                    "header": "New threads",
                    "pop_threads": threads[0:6],
                },
            )
        return loader.render_to_string(
            self.prerender_template,
            context={
                "header": "Most popular",
                "pop_threads": most_popular_threads[0:6],
            },
        )
