import logging

from django.core.cache import cache
from django.shortcuts import render
from django.template import loader
from django.views import View

from forum.user_verification import user_verification

logger = logging.getLogger(__name__)


class BaseView(View):
    template_name = "base.html"
    prerender_template = None
    form_class = None
    cache_location = None

    @user_verification(user_needed=False)
    def get(self, request, *args, **kwargs):
        return self._get_rendered_view(
            request,
            kwargs.get("user"),
            prerender=self._get_prerender_from_cache(*args, **kwargs)
            if self.cache_location else self._get_prerender_view(*args, **kwargs),
        )

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

    def _get_prerender_from_cache(self, *args, **kwargs):
        print(kwargs)
        true_cache_location = self.cache_location + "/" + kwargs.get("suffix", "")
        if cached := cache.get(true_cache_location):
            logger.info(f"Getting {true_cache_location} from cache")
            return cached
        else:
            prerender = self._get_prerender_view(*args, **kwargs)
            logger.info(f"Setting {true_cache_location} to cache")
            cache.set(true_cache_location, prerender, 30*60)
            return prerender

    def _get_prerender_view(self, *args, **kwargs):
        raise NotImplemented

    def clear_cache(self, suffix=""):
        true_cache_location = self.cache_location + "/" + suffix
        logger.info(f"Resetting {self.cache_location}{suffix} cache")
        cache.set(true_cache_location, None)
