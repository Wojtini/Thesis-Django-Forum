from django.shortcuts import render
from django.views import View

from forum import models
from forum.user_verification import user_verification


class Index(View):
    template_name = "index.html"

    @user_verification
    def get(self, request, *args, **kwargs):
        user = kwargs.get("user")
        return self._get_rendered_view(request, user)

    def _get_rendered_view(self, request, user):
        return render(
            request,
            self.template_name,
            context={
                "user": user,
                "threads": sorted(models.Thread.objects.all(), key=lambda t: t.update_date, reverse=True)[0:3],
            },
        )
