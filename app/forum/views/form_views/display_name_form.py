from django.shortcuts import render
from django.views import View

from forum.forms import DisplayNameForm
from forum.decorators.user_verification import user_verification


class DisplayNameFormView(View):
    form_class = DisplayNameForm

    @user_verification(user_needed=False)
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "components/form.html",
            context={
                "form": self.form_class,
                "endpoint": f"displaynameform/",
            }
        )

    @user_verification(user_needed=True)
    def post(self, request, *args, **kwargs):
        user = kwargs.get("user")
        form = self.form_class(request.POST)
        if form.is_valid():
            if not user.display_name:
                user.display_name = form.cleaned_data["display_name"]
                user.save()
        return render(request, "components/reload_page.html")
