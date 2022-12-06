from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views import View

from forum import models
from forum.forms import ThreadForm
from forum.models import Thread
from forum.decorators.user_verification import user_verification


class ThreadFormView(View):
    form_class = ThreadForm

    @user_verification(user_needed=False)
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "components/form.html",
            context={
                "form": self.form_class,
                "endpoint": f"threadform/{kwargs.get('category_name')}",
            }
        )

    @user_verification(user_needed=True)
    def post(self, request, *args, **kwargs):
        category = models.Category.objects.get(name=kwargs.get("category_name"))
        form = self.form_class(request.POST, request.FILES)
        user = kwargs.get("user")
        if form.is_valid():
            thread_name = form.cleaned_data.get("title")
            try:
                existing_thread = Thread.objects.get(title=thread_name)
                form.add_error("title", f"Title already exists with {existing_thread}!")
            except ObjectDoesNotExist:
                new_thread = Thread(
                    title=thread_name,
                    creator=user,
                    description=form.cleaned_data.get("description"),
                    category=category,
                )
                new_thread.save()
                return render(request, "components/thread.html", context={"thread": new_thread})
        if kwargs.get("new_user"):
            return render(request, "components/reload_page.html")
        return render(
            request,
            "components/form.html",
            context={
                "form": form,
                "endpoint": f"threadform/{kwargs.get('category_name')}",
            }
        )
