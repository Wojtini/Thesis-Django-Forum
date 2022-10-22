from django.shortcuts import render
from django.views import View
from forum.models import Image


class GalleryView(View):
    template_name = "gallery.html"

    def get(self, request, *args, **kwargs):
        images = [image for image in Image.objects.filter(entry__thread__indexed=True)]
        return render(
            request,
            self.template_name,
            context={
                "user": kwargs.get("user"),
                "images": images,
            }
        )
