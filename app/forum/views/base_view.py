import logging

from django.core.cache import cache
from django.shortcuts import render
from django.views import View

from Masquerade.settings import DISABLE_CACHE
from forum.decorators.rule_accepter import must_accept_rules
from forum.decorators.user_verification import user_verification

logger = logging.getLogger(__name__)


class BaseView(View):
    template_name = "base/base.html"
    prerender_template = None
    cache_location = None

    @must_accept_rules
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
                **additional_context,
            },
        )

    def _get_prerender_from_cache(self, *args, **kwargs):
        if DISABLE_CACHE:
            logger.info(f"Cache disabled, recreating view")
            return self._get_prerender_view(*args, **kwargs)
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
        if self.cache_location:
            true_cache_location = self.cache_location + "/" + suffix
            logger.info(f"Resetting cache at {true_cache_location} location")
            cache.set(true_cache_location, None)
