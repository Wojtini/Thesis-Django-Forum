from django.shortcuts import render
from django.views import View

from forum.forms import CategoryForm
from forum.models import Category
from forum.user_verification import user_verification


class CategoryView(View):
    template_name = "category.html"
    form_class = CategoryForm

    @user_verification
    def get(self, request, *args, **kwargs):
        user = kwargs.get("user")
        return self._get_rendered_view(request, user, self.form_class)

    @user_verification
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        user = kwargs.get("user")
        if form.is_valid():
            new_category = Category(
                name=form.cleaned_data.get("name"),
                creator=user,
            )
            new_category.save()
        return self._get_rendered_view(request, user, form)

    def _get_rendered_view(self, request, user, form):
        return render(
            request,
            self.template_name,
            context=
            {
                "user": user,
                "categories": Category.all_non_empty,
                "form": form,
            }
        )
