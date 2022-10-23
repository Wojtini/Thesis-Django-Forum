from io import BytesIO

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.files import File
from django.http import HttpResponseRedirect
from django.template import loader

from Masquerade.settings import THREAD_CACHE
from forum import models
from forum.forms import EntryForm
from forum.models import Entry, EntryFile
from PIL import Image as PImage

from forum.user_verification import user_verification
from forum.views import GalleryView
from forum.views.base_view import BaseView


class ThreadView(BaseView):
    prerender_template = "thread_content.html"
    form_class = EntryForm
    cache_location = THREAD_CACHE

    @user_verification(user_needed=False)
    def get(self, request, *args, **kwargs):
        kwargs.update({"suffix": kwargs.get("thread_name")})
        return self._get_rendered_view(
            request,
            kwargs.get("user"),
            prerender=self._get_prerender_from_cache(*args, **kwargs)
            if self.cache_location else self._get_prerender_view(*args, **kwargs),
        )

    def _get_prerender_view(self, *args, **kwargs):
        thread = models.Thread.objects.get(title=kwargs.get("thread_name"))
        return loader.render_to_string(
            self.prerender_template,
            context={
                "thread": thread,
            },
        )

    @user_verification(user_needed=True)
    def post(self, request, *args, **kwargs):
        user = kwargs.get("user")
        thread = models.Thread.objects.get(title=kwargs.get("thread_name"))
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist("files")
            entry = self._create_new_entry(user, thread, form, files)
            self._update_connected_clients(entry)
            print(request.path_info)
            return HttpResponseRedirect(request.path_info + f"#{entry.id}")

        kwargs.update({"suffix": kwargs.get("thread_name")})
        prerender = self._get_prerender_view(*args, **kwargs)
        return self._get_rendered_view(
            request,
            user,
            prerender,
            additional_context={"form_message": form.errors},
        )

    def _create_new_entry(self, user, thread, form, files) -> Entry:
        new_entry = Entry(
            creator=user,
            thread=thread,
            content=str(form.cleaned_data["content"]),
            replied_to=None,
        )
        new_entry.save()
        for file in files:
            new_file = ThreadView._create_new_file(file)
            new_entry.attached_files.add(new_file)
        self.clear_cache(thread.title)
        return new_entry

    @staticmethod
    def _create_new_file(file) -> EntryFile:
        new_file = EntryFile(
            original_file=file,
        )
        new_file.save()
        if new_file.is_image:
            compressed = ThreadView._compress(file, 256)
            new_file.compressed_file = compressed
            new_file.save()
            GalleryView().clear_cache()
        return new_file

    @staticmethod
    def _update_connected_clients(entry: Entry):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            str(entry.thread_id),
            {
                "type": "update_thread",
                "content": loader.render_to_string("entry.html", {"entry": entry}),
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
