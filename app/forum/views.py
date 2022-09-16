import datetime

from django.shortcuts import render
from django.views import View

from forum.user_verification import user_verification


class Index(View):
    template_name = "index.html"

    @user_verification
    def get(self, request, *args, **kwargs):
        response = render(request, self.template_name)
        return response

  # def post(self, request, *args, **kwargs):
  #   form = self.form_class(request.POST)
  #   if form.is_valid():
  #     form.save()
  #     return HttpResonseRedirect(reverse('list-view'))
  #   else:
  #     return render(request, self.template_name, {'form': form})