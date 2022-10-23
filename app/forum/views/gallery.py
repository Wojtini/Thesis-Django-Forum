import logging

from django.template import loader

from Masquerade.settings import GALLERY_CACHE
from forum.models import EntryFile
from forum.views.base_view import BaseView

logger = logging.getLogger(__name__)


class GalleryView(BaseView):
    prerender_template = "gallery.html"
    cache_location = GALLERY_CACHE

    def _get_prerender_view(self, *args, **kwargs):
        return loader.render_to_string(
            self.prerender_template,
            context={
                "images": [file for file in EntryFile.objects.all() if file.is_image],
            },
        )
