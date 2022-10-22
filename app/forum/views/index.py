from forum import models
from forum.views.base_view import BaseView


class Index(BaseView):
    prerender_template = "index.html"

    def get(self, request, *args, **kwargs):
        user = kwargs.get("user")
        threads = sorted(models.Thread.objects.filter(indexed=True), key=lambda t: t.update_date, reverse=True)[0:3]
        prerender = self._get_prerender_view(
            context={
                "threads": threads,
            }
        )
        return self._get_rendered_view(
            request,
            user,
            prerender=prerender,
        )
