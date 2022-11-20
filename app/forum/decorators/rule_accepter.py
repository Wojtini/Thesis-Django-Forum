from django.shortcuts import redirect

from Masquerade.settings import COOKIE_NAME_RULES


def must_accept_rules(function):
    def decorator(*args, **kwargs):
        request = args[0].request
        if COOKIE_NAME_RULES in request.COOKIES:
            return function(*args, **kwargs)
        return redirect("/rules")
    return decorator
