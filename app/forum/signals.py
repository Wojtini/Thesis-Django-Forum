import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from forum.models import Entry, EntryFile
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
