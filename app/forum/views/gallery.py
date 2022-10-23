import logging

from Masquerade.settings import GALLERY_CACHE
from forum.models import EntryFile
from forum.user_verification import user_verification
from forum.views.base_view import BaseView

logger = logging.getLogger(__name__)


class GalleryView(BaseView):
    prerender_template = "gallery.html"
    cache_location = GALLERY_CACHE

    @user_verification(user_needed=False)
    def get(self, request, *args, **kwargs):
        return self._get_rendered_view(
            request,
            kwargs.get("user"),
            prerender=self._get_prerender_view(
                context={
                    "images": [file for file in EntryFile.objects.all() if file.is_image],
                }
            ),
        )
