from django.shortcuts import render
from django.views import View

from forum import models
from forum.forms import ThreadForm
from forum.models import Thread
from forum.user_verification import user_verification


class Index(View):
    template_name = "index.html"
    form_class = ThreadForm

    @user_verification
    def get(self, request, *args, **kwargs):
        user = kwargs.get("user")
        return self._get_rendered_view(request, user, self.form_class)

    @user_verification
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        user = kwargs.get("user")
        if form.is_valid():
            new_thread = Thread(
                title=form.cleaned_data.get("title"),
                creator=user,
                description=form.cleaned_data.get("description"),
                category=form.cleaned_data.get("category"),
            )
            new_thread.save()
        return self._get_rendered_view(request, user, form)

    def _get_rendered_view(self, request, user, form):
        return render(
            request,
            self.template_name,
            context={
                "user": user,
                "threads": models.Thread.objects.all(),
                "form": form,
            },
        )
