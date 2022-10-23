import logging

from django.core.cache import cache
from django.shortcuts import render
from django.template import loader
from django.views import View


logger = logging.getLogger(__name__)


class BaseView(View):
    template_name = "base.html"
    prerender_template = None
    form_class = None
    cache_location = None

    def _get_rendered_view(self, request, user, prerender, additional_context=None):
        if additional_context is None:
            additional_context = {}
        return render(
            request,
            self.template_name,
            context={
                "user": user,
                "prerender": prerender,
                "form": self.form_class,
                **additional_context,
            },
        )

    def _get_prerender_from_cache(self, context, suffix=""):
        if self.cache_location and (cached := cache.get(self.cache_location)):
            logger.info("Getting from cache")
            return cached
        else:
            prerender = self._get_prerender_view(context=context)
            logger.info(f"Setting gallery's images to cache")
            cache.set(self.cache_location + suffix, prerender, 30*60)
            return prerender

    def _get_prerender_view(self, context):
        if not self.prerender_template:
            return ""
        return loader.render_to_string(
            self.prerender_template,
            context=context,
        )

    def clear_cache(self, suffix=""):
        logger.info(f"Resseting {self.cache_location}{suffix} cache")
        cache.set(self.cache_location + suffix, None)
