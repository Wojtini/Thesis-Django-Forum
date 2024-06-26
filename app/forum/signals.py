import logging
import os

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from forum.models import Entry, EntryFile, User, Thread
from forum.views import ThreadView, GalleryView, FileListView, UserListView

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Entry, dispatch_uid="clear_thread_cache")
def clear_thread_cache(sender, instance: Entry, **kwargs):
    ThreadView().clear_cache(instance.thread.title)
    UserListView().clear_cache()


@receiver(post_save, sender=EntryFile, dispatch_uid="clear_gallery_cache")
def clear_gallery_cache(sender, instance: EntryFile, **kwargs):
    if instance.is_image:
        GalleryView().clear_cache()
    FileListView().clear_cache()


# File Deletion

@receiver(post_delete, sender=Thread)
def clear_thread_cache_upon_deletion(sender, instance: Thread, **kwargs):
    ThreadView().clear_cache()


@receiver(post_delete, sender=EntryFile)
def auto_delete_file_on_delete(sender, instance: EntryFile, **kwargs):
    if instance.original_file and os.path.isfile(instance.original_file.path):
        try:
            os.remove(instance.original_file.path)
        except FileNotFoundError:
            pass
    if instance.compressed_file and os.path.isfile(instance.compressed_file.path):
        try:
            os.remove(instance.compressed_file.path)
        except FileNotFoundError:
            pass


@receiver(post_delete, sender=User)
def auto_delete_file_on_delete(sender, instance: User, **kwargs):
    if instance.identicon and os.path.isfile(instance.identicon.path):
        os.remove(instance.identicon.path)
