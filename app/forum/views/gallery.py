import asyncio
import logging

from django.shortcuts import render
from django.views import View

from forum.models import Image
from django.core.cache import cache

from forum.user_verification import user_verification
from forum.views.base_view import BaseView

logger = logging.getLogger(__name__)


class GalleryView(BaseView):
    prerender_template = "gallery.html"

    @user_verification(user_needed=False)
    def get(self, request, *args, **kwargs):
        # if cached := cache.get('images'):
        #     logger.info("Getting from cache")
        #     prerender = cached
        # else:
        #     # images = [image for image in Image.objects.all()]
        #     prerender = self._get_prerender_view(
        #         context={
        #             "images": [image for image in Image.objects.all()],
        #         }
        #     )
        #     logger.info(f"Setting gallery's images to cache")
        #     cache.set('images', prerender, 30*60)
        prerender = self._get_prerender_view(
            context={
                "images": [image for image in Image.objects.all()],
            }
        )
        return self._get_rendered_view(
            request,
            kwargs.get("user"),
            prerender=prerender,
        )
