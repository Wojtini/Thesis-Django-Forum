from django.db.models import Sum, Max
from django.template import loader

from forum import models
from forum.views.base_view import BaseView


class IndexView(BaseView):
    prerender_template = "index.html"
    cache_location = None

    def _get_prerender_view(self, *args, **kwargs):
        most_popular_threads = models.Thread.objects.annotate(pop_max=Max("cyclethread__popularity")).order_by("-pop_max")[0:6]

        last_activity_threads = models.Thread.objects.all()
        last_activity_threads = sorted(last_activity_threads, key=lambda x: x.update_date, reverse=True)

        return loader.render_to_string(
            self.prerender_template,
            context={
                "pop_threads": most_popular_threads,
                "act_threads": last_activity_threads,
            },
        )
