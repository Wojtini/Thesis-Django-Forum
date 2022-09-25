import datetime

from django.shortcuts import render
from django.views import View

from forum.user_verification import user_verification


class Index(View):
    template_name = "index.html"

    @user_verification
    def get(self, request, *args, **kwargs):
        response = render(request, self.template_name, context={"user": kwargs.get("user")})
        return response
