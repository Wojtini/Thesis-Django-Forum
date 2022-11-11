import logging
import os

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from forum.models import Entry, EntryFile, User
from forum.views import ThreadView, GalleryView, FileListView, UserListView

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Entry, dispatch_uid="clear_thread_cache")
def clear_thread_cache(sender, instance: Entry, **kwargs):
    ThreadView().clear_cache(instance.thread.title)
    UserListView().clear_cache()


@receiver(post_save, sender=EntryFile, dispatch_uid="clear_gallery_cache")
def clear_gallery_cache(sender, instance: EntryFile, **kwargs):
    GalleryView().clear_cache()
    FileListView().clear_cache()


@receiver(post_delete, sender=EntryFile)
def auto_delete_file_on_delete(sender, instance: EntryFile, **kwargs):
    if instance.original_file and os.path.isfile(instance.original_file.path):
        os.remove(instance.original_file.path)
    if os.path.isfile(instance.compressed_file.path):
        os.remove(instance.compressed_file.path)


@receiver(post_delete, sender=User)
def auto_delete_file_on_delete(sender, instance: User, **kwargs):
    if instance.identicon and os.path.isfile(instance.identicon.path):
        os.remove(instance.identicon.path)


@receiver(post_delete, sender=Entry)
def auto_delete_file_on_delete(sender, instance: User, **kwargs):
    if instance.identicon and os.path.isfile(instance.identicon.path):
        os.remove(instance.identicon.path)

