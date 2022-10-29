import logging

from django.template import loader

from forum.models import User
from forum.views.base_view import BaseView

logger = logging.getLogger(__name__)


class UserEntriesView(BaseView):
    prerender_template = "userentries.html"

    def _get_prerender_view(self, *args, **kwargs):
        user = User.objects.get(identifier=kwargs.get("user_id"))
        return loader.render_to_string(
            self.prerender_template,
            context={
                "user": user,
            },
        )
