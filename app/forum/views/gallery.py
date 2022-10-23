import logging

from forum.models import EntryFile
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
                "images": [file for file in EntryFile.objects.all() if file.is_image],
            }
        )
        return self._get_rendered_view(
            request,
            kwargs.get("user"),
            prerender=prerender,
        )
