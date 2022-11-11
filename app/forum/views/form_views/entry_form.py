from io import BytesIO

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views import View

from forum.forms import EntryForm
from forum.models import Entry, EntryFile, Thread, User
from PIL import Image as PImage

from forum.user_verification import user_verification


class EntryFormView(View):
    form_class = EntryForm

    @user_verification(user_needed=False)
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "components/form.html",
            context={
                "form": self.form_class,
                "endpoint": f"entryform/{kwargs.get('thread_name')}",
            }
        )

    @user_verification(user_needed=True)
    def post(self, request, *args, **kwargs):
        user = kwargs.get("user")
        thread = Thread.objects.get(title=kwargs.get("thread_name"))
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist("files")
            entry = self._create_new_entry(user, thread, form, files)
            self._update_connected_clients(entry, user)
        else:
            return render(
                request,
                "components/form.html",
                context={
                    "form_errors": form.errors,
                    "form": form,
                    "endpoint": f"entryform/{kwargs.get('thread_name')}",
                }
            )
        print(form.errors)
        return HttpResponse(status=204)

    def _create_new_entry(self, user, thread, form, files) -> Entry:
        new_entry = Entry(
            creator=user,
            thread=thread,
            content=str(form.cleaned_data["content"]),
        )
        new_entry.save()
        for file in files:
            EntryFormView._create_new_file(file, new_entry)
        return new_entry

    @staticmethod
    def _create_new_file(file, new_entry) -> EntryFile:
        new_file = EntryFile(
            entry=new_entry,
            original_file=file,
        )
        new_file.save()
        if new_file.is_image:
            compressed = EntryFormView._compress(file, 256)
            new_file.compressed_file = compressed
            new_file.save()
        return new_file

    @staticmethod
    def _update_connected_clients(entry: Entry, user: User):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            str(entry.thread_id),
            {
                "type": "update_thread",
                "content": loader.render_to_string("components/entry.html", {"entry": entry}),
                "origin_user": str(user.identifier),
            },
        )

    @staticmethod
    def _compress(image, size) -> File:
        size = size, size
        im = PImage.open(image)
        im_io = BytesIO()
        im.thumbnail(size, PImage.ANTIALIAS)
        im = im.convert('RGB')
        im.save(im_io, 'JPEG', quality=60)
        new_image = File(im_io, name=image.name)
        return new_image
