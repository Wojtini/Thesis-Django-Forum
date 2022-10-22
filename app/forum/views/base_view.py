from django.shortcuts import render
from django.template import loader
from django.views import View


class BaseView(View):
    template_name = "base.html"
    prerender_template = None
    form_class = None

    def _get_rendered_view(self, request, user, prerender, additional_context=None):
        if additional_context is None:
            additional_context = {}
        return render(
            request,
            self.template_name,
            context={
                "user": user,
                "prerender": prerender,
                "form": self.form_class,
                **additional_context,
            },
        )

    def _get_prerender_view(self, context):
        if not self.prerender_template:
            return ""
        return loader.render_to_string(
            self.prerender_template,
            context=context,
        )
