from django.shortcuts import render
from django.views import View

from forum.forms import CategoryForm
from forum.models import Category
from forum.user_verification import user_verification
from forum.views.base_view import BaseView


class CategoryListView(BaseView):
    prerender_template = "categories_list.html"
    form_class = CategoryForm

    @user_verification
    def get(self, request, *args, **kwargs):
        user = kwargs.get("user")
        prerender = self._get_prerender_view(
            context={
                "categories": Category.all_non_empty,
            }
        )
        return self._get_rendered_view(request, user, prerender)

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
        prerender = self._get_prerender_view(
            context={
                "categories": Category.all_non_empty,
            }
        )
        return self._get_rendered_view(request, user, prerender)
