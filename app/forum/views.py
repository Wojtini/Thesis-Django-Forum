import datetime
from io import BytesIO

from django.core.files import File
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from forum import models
from forum.forms import EntryForm
from forum.models import Image, Entry
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
            content = form.cleaned_data["content"]
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
                content=content,
                attached_image=new_img,
                replied_to=None,
            )
            new_entry.save()
            return HttpResponseRedirect(request.path_info)

        return render(request, self.template_name, {'form': form})


def compress(image):
    size = 128, 128
    im = PImage.open(image)
    im_io = BytesIO()
    im.thumbnail(size, PImage.ANTIALIAS)
    im.save(im_io, 'JPEG', quality=60)
    new_image = File(im_io, name=image.name)
    return new_image
