from io import BytesIO

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.files import File
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.views import View
from django.views.decorators.csrf import csrf_protect

from forum import models
from forum.forms import EntryForm
from forum.models import Image, Entry, Category
from PIL import Image as PImage
from forum.user_verification import user_verification


class Index(View):
    template_name = "index.html"

    @user_verification
    def get(self, request, *args, **kwargs):
        try:
            threads_list = models.Thread.objects.all()
        except:
            threads_list = []
        return render(
            request,
            self.template_name,
            context={
                "user": kwargs.get("user"),
                "threads": threads_list
            },
        )


class ThreadView(View):
    template_name = "thread.html"
    form_class = EntryForm

    @user_verification
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        thread_id = kwargs.get("thread_id")
        thread = models.Thread.objects.get(id=thread_id)
        entries = thread.entries

        return render(
            request,
            self.template_name,
            context=
            {
                "user": kwargs.get("user"),
                "thread": thread,
                "entries": entries,
                "form": form,
            }
        )

    @user_verification
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            thread_id = kwargs.get("thread_id")
            img = form.cleaned_data.get("image")
            new_img = Image(
                name="Test",
                user=None,
                original_file=img,
                compressed_file=compress(img),
            )
            new_img.save()
            new_entry = Entry(
                creator=kwargs.get("user"),
                thread=models.Thread.objects.get(id=thread_id),
                content=form.cleaned_data["content"],
                attached_image=new_img,
                replied_to=None,
            )
            new_entry.save()

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                str(thread_id),
                {
                    "type": "update_thread",
                    "content": loader.render_to_string("entry.html", {"entry": new_entry}),
                },
            )

            return HttpResponseRedirect(request.path_info)

        return render(request, self.template_name, {"form": form})


class CategoryView(View):
    template_name = "category.html"

    @user_verification
    def get(self, request, *args, **kwargs):
        data = {
            category: category.threads
            for category in Category.objects.all()
            if not category.is_empty
        }
        return render(
            request,
            self.template_name,
            context=
            {
                "user": kwargs.get("user"),
                "data": data,
            }
        )


class GalleryView(View):
    template_name = "gallery.html"

    def get(self, request, *args, **kwargs):
        images = [image for image in Image.objects.all()]
        return render(
            request,
            self.template_name,
            context=
            {
                "user": kwargs.get("user"),
                "images": images,
            }
        )


def compress(image):
    size = 128, 128
    im = PImage.open(image)
    im_io = BytesIO()
    im.thumbnail(size, PImage.ANTIALIAS)
    im = im.convert('RGB')
    im.save(im_io, 'JPEG', quality=60)
    new_image = File(im_io, name=image.name)
    return new_image
