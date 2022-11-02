from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from forum import models
from forum.forms import ThreadForm
from forum.models import Thread
from forum.user_verification import user_verification


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
                "additional_arguments": 'hx-swap="afterbegin" hx-target="#thread_list"',
            }
        )

    @user_verification(user_needed=True)
    def post(self, request, *args, **kwargs):
        category = models.Category.objects.get(name=kwargs.get("category_name"))
        form = self.form_class(request.POST, request.FILES)
        user = kwargs.get("user")
        if form.is_valid():
            new_thread = Thread(
                title=form.cleaned_data.get("title"),
                creator=user,
                description=form.cleaned_data.get("description"),
                category=category,
            )
            new_thread.save()
            return render(request, "components/thread.html", context={"thread": new_thread})
        print(form.errors)
