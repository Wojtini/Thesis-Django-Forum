from django.db.models import Count
from django.template import loader

from forum.models import Category
from forum.decorators.user_verification import user_verification
from forum.views.base_view import BaseView


class CategoryListView(BaseView):
    prerender_template = "categories_list.html"

    def _get_prerender_view(self, *args, **kwargs):
        return loader.render_to_string(
            self.prerender_template,
            context={
                "categories": Category.objects.all().annotate(thread_count=Count('thread')).order_by('-thread_count'),
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
        prerender = self._get_prerender_view(*args, **kwargs)
        return self._get_rendered_view(request, user, prerender)
