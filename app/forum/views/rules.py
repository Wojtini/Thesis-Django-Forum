from django.shortcuts import redirect, render
from django.views import View

from Masquerade.settings import COOKIE_NAME_RULES, COOKIE_LIFETIME


class RulesView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "rules.html")

    def post(self, request, *args, **kwargs):
        response = redirect('/')
        response.set_cookie(COOKIE_NAME_RULES, 'Yes', COOKIE_LIFETIME)
        return response
