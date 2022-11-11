from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from forum.forms import CategoryForm
from forum.user_verification import user_verification


class CategoryFormView(View):
    form_class = CategoryForm

    @user_verification(user_needed=False)
    def delete(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return render(
                request,
                "components/form.html",
                context={
                    "form": self.form_class,
                    "endpoint": f"categoryform/",
                    "additional_arguments": 'hx-swap="afterbegin" hx-target="#categories_list"',
                }
            )
        else:
            return HttpResponse(status=404)
