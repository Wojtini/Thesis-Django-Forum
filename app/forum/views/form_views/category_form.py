from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from forum.forms import CategoryForm
from forum.models import Category
from forum.user_verification import user_verification


class CategoryFormView(View):
    form_class = CategoryForm

    @user_verification(user_needed=False)
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "components/form.html",
            context={
                "form": self.form_class,
                "endpoint": f"categoryform/",
                "additional_arguments": 'hx-swap="afterbegin" hx-target="#categories_list"',
            }
        )

    @user_verification(user_needed=True)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        user = kwargs.get("user")
        if form.is_valid():
            new_category = Category(
                name=form.cleaned_data.get("name"),
                creator=user,
            )
            new_category.save()
            return render(request, "components/category_panel.html", context={"category": new_category})
        print(form.errors)
        return HttpResponse(204)
