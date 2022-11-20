from django.http import HttpResponseRedirect
from django.views import View

from forum.decorators.user_verification import user_verification


class AccountCreation(View):
    @user_verification(user_needed=True)
    def get(self, request, *args, **kwargs):
        print(request.path_info)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
