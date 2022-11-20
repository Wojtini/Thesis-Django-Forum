from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views import View

from forum.forms import CategoryForm
from forum.models import Category
from forum.decorators.user_verification import user_verification


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
            }
        )

    @user_verification(user_needed=True)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        user = kwargs.get("user")
        if form.is_valid():
            category_name = form.cleaned_data.get("name")
            try:
                existing_category = Category.objects.get(name=category_name)
                form.add_error("name", f"Category already exists with {existing_category.name} name!")
            except ObjectDoesNotExist:
                new_category = Category(
                    name=category_name,
                    creator=user,
                )
                new_category.save()
                return render(
                    request, "components/category_panel.html",
                    context={
                        "category": new_category,
                        "additional_class": "bg-info"
                    }
                )

        return render(
            request,
            "components/form.html",
            context={
                "form": form,
                "endpoint": f"categoryform/",
            }
        )
