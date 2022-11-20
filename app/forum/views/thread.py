from django.template import loader

from Masquerade.settings import THREAD_CACHE
from forum import models

from forum.decorators.user_verification import user_verification
from forum.views.graph import GraphView
from forum.views.base_view import BaseView


class ThreadView(BaseView):
    prerender_template = "thread_content.html"
    cache_location = THREAD_CACHE

    @user_verification(user_needed=False)
    def get(self, request, *args, **kwargs):
        kwargs.update({"suffix": kwargs.get("thread_name")})
        return self._get_rendered_view(
            request,
            kwargs.get("user"),
            prerender=self._get_prerender_from_cache(*args, **kwargs)
            if self.cache_location else self._get_prerender_view(*args, **kwargs),
        )

    def _get_prerender_view(self, *args, **kwargs):
        thread = models.Thread.objects.get(title=kwargs.get("thread_name"))
        return loader.render_to_string(
            self.prerender_template,
            context={
                "thread": thread,
                "graph": GraphView().get_as_component_for_thread(thread)
            },
        )
