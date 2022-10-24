from django.http import HttpResponseRedirect
from django.template import loader

from forum.forms import CategoryForm
from forum.models import Category
from forum.user_verification import user_verification
from forum.views.base_view import BaseView


class CategoryListView(BaseView):
    prerender_template = "categories_list.html"
    form_class = CategoryForm

    def _get_prerender_view(self, *args, **kwargs):
        return loader.render_to_string(
            self.prerender_template,
            context={
                "categories": Category.objects.all(),
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
            return HttpResponseRedirect(request.path_info)
        prerender = self._get_prerender_view()
        return self._get_rendered_view(request, user, prerender, additional_context={"form_message": "Invalid Data"})
