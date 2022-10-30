from django.http import HttpResponseRedirect
from django.template import loader

from forum import models
from forum.forms import ThreadForm
from forum.models import Thread
from forum.user_verification import user_verification
from forum.views.base_view import BaseView


class CategoryView(BaseView):
    prerender_template = "category.html"
    form_class = ThreadForm

    def _get_prerender_view(self, *args, **kwargs):
        category = models.Category.objects.get(name=kwargs.get("category_name"))
        return loader.render_to_string(
            self.prerender_template,
            context={
                "category": category,
                "threads": sorted(models.Thread.objects.filter(category=category, indexed=True), key=lambda t: t.update_date, reverse=True),
            },
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
                indexed=True,
            )
            new_thread.save()
            return HttpResponseRedirect(request.path_info)
        prerender = self._get_prerender_view()
        return self._get_rendered_view(request, user, prerender, additional_context={"form_message": "Invalid Data"})
