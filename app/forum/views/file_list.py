import logging

from django.template import loader

from Masquerade.settings import FILE_LIST_CACHE
from forum.models import EntryFile
from forum.views.base_view import BaseView

logger = logging.getLogger(__name__)


class FileListView(BaseView):
    prerender_template = "filelist.html"
    cache_location = FILE_LIST_CACHE

    def _get_prerender_view(self, *args, **kwargs):
        return loader.render_to_string(
            self.prerender_template,
            context={
                "files": [file for file in EntryFile.objects.all()],
            },
        )
