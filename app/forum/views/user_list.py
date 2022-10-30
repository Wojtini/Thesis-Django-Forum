import logging

from django.template import loader

from Masquerade.settings import USER_LIST_CACHE
from forum.models import User
from forum.views.base_view import BaseView

logger = logging.getLogger(__name__)


class UserListView(BaseView):
    prerender_template = "userlist.html"
    cache_location = USER_LIST_CACHE

    def _get_prerender_view(self, *args, **kwargs):
        users = sorted([
            user
            for user in User.objects.all()
            if user.entries_amount != 0
        ], key=lambda x: x.entries_amount, reverse=True)
        return loader.render_to_string(
            self.prerender_template,
            context={
                "users": users,
            },
        )
