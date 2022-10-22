from django.shortcuts import render

from forum import models
from forum.forms import ThreadForm
from forum.models import Thread
from forum.user_verification import user_verification
from forum.views.base_view import BaseView


class CategoryView(BaseView):
    prerender_template = "category.html"
    form_class = ThreadForm

    @user_verification
    def get(self, request, *args, **kwargs):
        user = kwargs.get("user")
        category = models.Category.objects.get(name=kwargs.get("category_name"))
        prerender = self._get_prerender_view(
            context={
                "category": category,
                "threads": sorted(models.Thread.objects.filter(category=category, indexed=True), key=lambda t: t.update_date, reverse=True),
            }
        )
        return self._get_rendered_view(request, user, prerender)

    @user_verification
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        form.indexed = True
        category = models.Category.objects.get(name=kwargs.get("category_name"))
        user = kwargs.get("user")
        if form.is_valid():
            new_thread = Thread(
                title=form.cleaned_data.get("title"),
                creator=user,
                description=form.cleaned_data.get("description"),
                category=form.cleaned_data.get("category"),
                indexed=form.cleaned_data.get("indexed"),
            )
            new_thread.save()
        prerender = self._get_prerender_view(
            context={
                "category": category,
                "threads": sorted(models.Thread.objects.filter(category=category, indexed=True), key=lambda t: t.update_date, reverse=True),
            }
        )
        return self._get_rendered_view(request, user, prerender)
